$(document).ready(() => {
    myTable = $('#myArticelSummaryTable').DataTable({
        "orderClasses": false,
        "responsive": true,
        "fixedHeader": true,
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-primary');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });
    myTable.clear().draw();
    $(".dataTables_empty").addClass("table-warning text-dark font-weight-bold");
    $(".dataTables_empty").text("資料載入中");
    $.ajax({
        'url': location.origin + "/managerPages/getFileDataSummary",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            d3Data = [];
            for (i in data) {
                myTable.row.add([
                    i,
                    data[i],
                ])
                d3Data.push({
                    "name": i,
                    "value": data[i]
                })
            }
            drawBarChart("articleBarChart", d3Data);
            drawPieChart("articlePieChart", d3Data);
            setTimeout(function () {
                myTable.draw(true);
                myTable.columns.adjust().draw();
                myTable.responsive.recalc().columns.adjust();
            }, 10);
        },
        'error': (res) => {
            alert("伺服器出狀況,請聯繫系統人員")
        }
    });

    rankTableHeadChinese = [
        "文章標題", "主類別", "評分", "兌換人數"
    ]
    $("#articleRankNav").on("click", () => {
        if ($.fn.DataTable.isDataTable("#articelRankTable")) {
            return;
        } else {
            rankTable = $('#articelRankTable').DataTable({
                "orderClasses": false,
                "order": [[3, "desc"]],
                "responsive": true,
                "fixedHeader": true,
                "language": {
                    url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
                },
                "createdRow": function (row, data, dataIndex) {
                    $(row).addClass('table-primary');
                    $(row).addClass('text-dark');
                    $(row).addClass('font-weight-bold');
                }
            });
        }

        rankTable.clear().draw();
        $(".dataTables_empty").addClass("table-warning text-dark font-weight-bold");
        $(".dataTables_empty").text("資料載入中");
        $.ajax({
            'url': location.origin + "/managerPages/getArticleOwnRank",
            'method': 'GET',
            'processData': false,
            'contentType': false,
            'headers': { 'X-CSRFToken': getCookie('csrftoken') },
            'success': (res) => {
                allData = JSON.parse(res)
                allData.sort((a, b) => Number(a['total']) > Number(b['total']))
                d3Data = [];
                for (i in allData) {
                    data = allData[i];
                    rankTable.row.add([
                        `<a target="_blank" href="${location.origin}/viewFilePage/${data['fileID']}">${data['title']}</a>`,
                        data['mainClass'],
                        Number(data['totalStars']),
                        data['total'],
                    ])
                    d3Data.push({
                        "name": data['title'],
                        "value": data['total']
                    })
                }
                rankTable.columns().every(function (index) {
                    if (rankTableHeadChinese[index] !== "主類別") {
                        return;
                    }
                    var column = this;
                    selectHTML = `
                    <div class="col-auto">
                        <label>${rankTableHeadChinese[index]}</label>
                        <select class="custom-select custom-select-md"><option value=""></option></select>
                    </div>
                    `
                    var select = $(selectHTML)
                        .appendTo($("#colSearch"));

                    select.find("select").on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();

                        // Update bar chart

                        currentData = rankTable.rows().data().filter((d) => { return d[1] == val || val == ""; })
                        d3Data = []
                        for (i = 0; i < currentData.length; i++) {
                            d3Data.push({
                                "name": $(currentData[i][0]).html(),
                                "value": Number(currentData[i][3])
                            })
                        }
                        d3Data.sort((a, b) => a.value > b.value);
                        drawHorizontalBarChart("rankBarChart", d3Data);
                    });

                    column.data().unique().sort().each(function (d, j) {
                        select.find("select").append('<option value="' + d + '">' + d + '</option>')
                    });
                });
                drawHorizontalBarChart("rankBarChart", d3Data);
                setTimeout(function () {
                    rankTable.draw(true);
                    rankTable.columns.adjust().draw();
                    rankTable.responsive.recalc().columns.adjust();
                }, 10);
            },
            'error': (res) => {
                alert("伺服器出狀況,請聯繫系統人員")
            }
        });
    })

    function drawPieChart(chartID, data) {
        var colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ];
        height = 300;
        width = 300;
        radius = width / 2;
        svg = d3.select("#" + chartID)
            .attr("viewBox", [0, 0, width, height])
            .append("g")
            .attr('transform', `translate(${width / 2}, ${height / 2})`);
        const arc = d3
            .arc()
            .innerRadius(radius * 0.5)
            .outerRadius(radius * 0.7)
        const pie = d3.pie().value(d => d.value)
        dataReady = pie(data)
        pieChart = svg.selectAll('path')
            .data(dataReady)
            .enter()
            .append('g');

        pieChart.append('path')
            .attr('fill', (d, i) => {
                return colors[i]
            }).transition()
            .delay(function(d,i) {
                return i * 100; })
            .duration(1000)
            .attrTween('d', function (d) {
                var i = d3.interpolate(d.startAngle + 0.1, d.endAngle);
                return function (t) {
                    d.endAngle = i(t);
                    return arc(d)
                }
            });

        pieChart.append("text")
            .attr("x", d => {
                return arc.centroid(d)[0]
            })
            .attr("y", d => arc.centroid(d)[1])
            .attr("font-size", "10px")
            .attr("fill", "white")
            .text(d => d.value);

        var outerArc = d3.arc()
            .innerRadius(radius * 0.8)
            .outerRadius(radius * 0.8)
        pieChart.selectAll('allPolylines')
            .data(dataReady)
            .enter()
            .append('polyline')
            .transition()
            .duration(2000)
            .attr("stroke", "white")
            .style("fill", "none")
            .attr("stroke-width", 1)
            .attr('points', function (d) {
                var posA = arc.centroid(d) // line insertion in the slice
                var posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
                var posC = outerArc.centroid(d); // Label position = almost the same as posB
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
                posC[0] = radius * 0.85 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
                return [posA, posB, posC]
            });

        pieChart.selectAll('allLabels')
            .data(dataReady)
            .enter()
            .append('text')
            .attr("font-size", "7px")
            .attr("fill", "white")
            .text(function (d) { return d.data.name })
            .attr('transform', function (d) {
                var pos = outerArc.centroid(d);
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                pos[0] = radius * 0.9 * (midangle < Math.PI ? 1 : -1);
                return 'translate(' + pos + ')';
            })
            .style('text-anchor', function (d) {
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                return (midangle < Math.PI ? 'start' : 'end')
            })
    }

    function drawBarChart(chartID, data) {

        title = {
            x: "Article",
            y: "sum"
        }
        margin = ({ top: 20, right: 20, bottom: 30, left: 40 });
        height = 300;
        width = 300;
        color = "steelblue";
        yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y).ticks(height / 40))
            .call(g => g.select(".domain").remove())
            .call(g => g.select(".tick:last-of-type text").clone()
                .attr("x", 4)
                .attr("text-anchor", "start")
                .attr("font-weight", "bold")
                .text(title.y));
        xAxis = g => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
            .call(g => g.append("text")
                .attr("x", width)
                .attr("y", -4)
                .attr("fill", "currentColor")
                .attr("font-weight", "bold")
                .attr("text-anchor", "end")
                .text(title.x));
        y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .range([height - margin.bottom, margin.top])

        x = d3.scalePoint()
            .domain(d3.map(data, d => d.name))
            .range([width - margin.right, margin.left])
            .padding(0.6)

        svg = d3.select("#" + chartID).attr("viewBox", [0, 0, width, height]);
        bar = svg.append("g")
            .attr("fill", color)
            .selectAll("rect")
            .data(data)
            .enter()
            .append("g");

        bar.append("rect")
            .attr("x", (d) => {
                return x(d.name) - 5
            })
            .attr("width", 10)
            .attr("y", d => y(0))
            .attr("height", d => y(0));

        bar.selectAll("rect")
            .transition()
            .duration(800)
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height-margin.bottom - y(d.value); })
            .delay(function(d,i){console.log(i) ; return(i*100)})

        bar.append("text")
            .attr("x", (d) => {
                return x(d.name)
            })
            .attr("y", d => y(d.value))
            .style("fill", "white")
            .attr("text-anchor", "middle")
            .attr("font-size", "11px")
            .text(d => d.value);

        svg.append("g")
            .call(xAxis);

        svg.append("g")
            .call(yAxis);
    }

    function drawHorizontalBarChart(chartID, data) {
        d3.select("#" + chartID).selectAll("svg > *").remove();
        data = data.slice(-10)
        title = {
            y: "",
            x: ""
        }
        margin = ({ top: 20, right: 20, bottom: 30, left: 40 });
        height = 350;
        width = 700;
        color = "steelblue";
        yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove())
            .call(g => g.selectAll("line").remove())
            .call(g => g.selectAll("text").text((d, i) => Math.abs(data.length - i)))

        xAxis = g => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))


        x = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .range([margin.left, width - margin.right])

        y = d3.scalePoint()
            .domain(d3.map(data, d => d.name))
            .range([height - margin.bottom, margin.top])
            .padding(0.6)

        svg = d3.select("#" + chartID).attr("viewBox", [0, 0, width, height]);

        bar = svg.append("g")
            .selectAll("rect")
            .data(data)
            .enter()
            .append("g");

        bar.append("rect")
            .attr("x", margin.left)
            .attr("y", (d) => {
                return y(d.name) - 5
            })
            .attr("height", 10)
            .transition() // and apply changes to all of them
            .duration(1000)
            .attr("fill", (d, i) => {
                return d3.schemeCategory10[i]
            })
            .attr("width", d => x(d.value) - x(0));

        bar.append("text")
            .attr("y", (d) => {
                return y(d.name) - 5
            })
            .attr("x", margin.left)
            .style("fill", "white")
            .style("text-anchor", "start")
            .style("font-size", "10px")
            .text(d => d.name);



        svg.append("g")
            .call(xAxis);

        svg.append("g")
            .call(yAxis)

    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});