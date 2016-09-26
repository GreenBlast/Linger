import sys
import os

PLUGIN_TEXT_TEMPLATE = \
"""[Core]
Name = %NAME_PLACEHOLDER%Factory
Module = %NAME_PLACEHOLDER%
    
[Documentation]
Description = %NAME_PLACEHOLDER%Factory creating instances of %NAME_PLACEHOLDER% which # TODO fill in
Author = Greenblast
Version = 1.0
Website = https://github.com/greenblast/linger/
"""

def main(plugin_name):
    plugin_text = PLUGIN_TEXT_TEMPLATE.replace("%NAME_PLACEHOLDER%", plugin_name)
    plugin_filename = ("%s.yapsy-plugin" % (plugin_name,))
    plugin_file = open("." + os.sep + plugin_filename,'w')
    plugin_file.write(plugin_text)
    plugin_file.flush()
    plugin_file.close()

if __name__ == '__main__':
    main(sys.argv[1])