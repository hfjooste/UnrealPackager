# Created by Henry Jooste
# https://github.com/hfjooste/UnrealPackager

from modules.setup import *

print()
print("==============================================")
print("| Unreal Packager v3.1.1                     |")
print("| Created by Henry Jooste                    |")
print("| https://github.com/hfjooste/UnrealPackager |")
print("==============================================")
print()

run_setup()

from modules.tasks import *
from modules.args import Args
from modules.config import Config

args = Args()
config = Config()

run_pre_task(config)
package_plugin(config)
package_project(config)
deploy_docs(config)
save_docs_pdf(config)
create_docs_zip(config)
create_release(args, config)
run_post_task(config)