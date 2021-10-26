app_name=server
project_dir=$(CURDIR)/../$(app_name)
build_dir=$(project_dir)/build
package_name=$(app_name)
version+=0.0.1


clean:
	rm -rf $(build_dir)

create-tag:
	git tag -s -a v$(version) -m "Tagging the $(version) release."
	git push origin v$(version)

production: clean 
	mkdir -p $(build_dir)/$(app_name)
	rsync -a \
	--exclude=/.babelrc.js \
	--exclude=/.drone.yml \
	--exclude=/.git \
	--exclude=/.gitattributes \
	--exclude=/.github \
	--exclude=/.gitignore \
	--exclude=/.php_cs.dist \
	--exclude=/.scrutinizer.yml \
	--exclude=/.travis.yml \
	--exclude=/.tx \
	--exclude=/CONTRIBUTING.md \
	--exclude=/Makefile \
	--exclude=/server/settings.py \
	--exclude=/README.md \
	--exclude=/build/sign \
	--exclude=/composer.json \
	--exclude=/composer.lock \
	--exclude=/docs \
	--exclude=/issue_template.md \
	--exclude=/l10n/l10n.pl \
	--exclude=/node_modules \
	--exclude=/package-lock.json \
	--exclude=/package.json \
	--exclude=/postcss.config.js \
	--exclude=/src \
	--exclude=/tests \
	--exclude=/translationfiles \
	--exclude=/tsconfig.json \
	--exclude=/vendor \
	--exclude=/build \
	--exclude='*/__pycache__' \
	--exclude='*/migrations' \
	--exclude=/webpack.* \
	$(project_dir)/ $(build_dir)/$(app_name)
	tar -czf $(build_dir)/$(app_name)-$(version).tar.gz \
		 -C $(build_dir) $(app_name)
	
