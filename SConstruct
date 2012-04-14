#
#Envrionment settings
#
env = Environment()
env['PROJECT_NAME'] = "sample" # CHANGE THIS VALUE TO YOUR PROJECT NAME
env['NAMESPACE'] = env['PROJECT_NAME'] + ".index" # CHANGE THIS

env['JAVA'] = "/usr/bin/java"
env['CLOSURE_PROJECT_DIR'] = "closure-project/"
env['CLOSURE_STYLESHEETS_JAR'] = env['CLOSURE_PROJECT_DIR'] + "closure-stylesheets/closure-stylesheets.jar"
env['CLOSURE_TEMPLATE_DIR'] = env['CLOSURE_PROJECT_DIR'] + "closure-templates/"
env['CLOSURE_TEMPLATE_JAR'] = env['CLOSURE_TEMPLATE_DIR'] + "SoyToJsSrcCompiler.jar"
env['CLOSURE_COMPILER_JAR'] = env['CLOSURE_PROJECT_DIR'] + "closure-compiler/compiler.jar"
env['CLOSURE_LIBRARY_ROOT_DIR'] = env['CLOSURE_PROJECT_DIR'] + "closure-library/"
env['DEPSWRITER'] = env['CLOSURE_LIBRARY_ROOT_DIR'] + "closure/bin/build/depswriter.py"
env['CLOSUREBUILDER'] = env['CLOSURE_LIBRARY_ROOT_DIR'] + "closure/bin/build/closurebuilder.py"

env['INPUT_STYLESHEET_DIR'] = "static/stylesheet/"
env['INPUT_JAVASCRIPT_DIR'] = "static/javascript/"
env['INPUT_TEMPLATE_DIR'] = "static/javascript/soy/"

env['OUTPUT_STYLESHEET_DIR'] = "_generated/stylesheet/"
env['OUTPUT_JAVASCRIPT_DIR'] = "_generated/javascript/"
env['OUTPUT_STYLESHEET_DEBUG_MAP'] = env['OUTPUT_JAVASCRIPT_DIR'] + "renaming_map_debug.js"
env['OUTPUT_STYLESHEET_DEBUG'] = env['OUTPUT_STYLESHEET_DIR'] + env['PROJECT_NAME'] + "_debug.css"
env['OUTPUT_STYLESHEET_RELEASE_MAP'] = env['OUTPUT_JAVASCRIPT_DIR'] + "renaming_map_release.js"
env['OUTPUT_STYLESHEET_RELEASE'] = env['OUTPUT_STYLESHEET_DIR'] + env['PROJECT_NAME'] + "_release.css"
env['OUTPUT_DEPS_JS'] = env['OUTPUT_JAVASCRIPT_DIR'] + "deps.js"
env['OUTPUT_JAVASCRIPT_DEBUG'] = "_generated/" + env['PROJECT_NAME'] +"_debug.js"
env['OUTPUT_JAVASCRIPT_RELEASE'] = "_generated/" + env['PROJECT_NAME'] +"_release.js"


def find_recursive(pattern, rootdirs):
  import fnmatch
  import os
  matches = []
  rootdirs = rootdirs if isinstance(rootdirs, type([])) else [rootdirs]
  for rootdir in rootdirs:
    for root, dirnames, filenames in os.walk(rootdir):
      for filename in fnmatch.filter(filenames, pattern):
          matches.append(os.path.join(root, filename))
  return matches

def build_command_string(prefix, item_format, list, suffix):
  return " ".join([prefix] + [item_format % {"item": item} for item in list] + [suffix])


#
# INPUT FILES
#
INPUT_STYLESHEET_FILES = find_recursive("*.gss", env['INPUT_STYLESHEET_DIR'])
INPUT_SOY_FILES = find_recursive("*.soy", env['INPUT_TEMPLATE_DIR'])
INPUT_JAVASCRIPT_FILES = find_recursive("*.js", [env['INPUT_JAVASCRIPT_DIR'], env['CLOSURE_LIBRARY_ROOT_DIR'], env['CLOSURE_TEMPLATE_DIR']])


#
# RULES
#
STYLESHEET_COMMAND_COMMON = "$JAVA -jar $CLOSURE_STYLESHEETS_JAR --output-file ${TARGETS[0]} --output-renaming-map ${TARGETS[1]} "
# STYLESHEET(DEBUG)
env.Command([env['OUTPUT_STYLESHEET_DEBUG'], env['OUTPUT_STYLESHEET_DEBUG_MAP']], INPUT_STYLESHEET_FILES,
    STYLESHEET_COMMAND_COMMON + "--output-renaming-map-format CLOSURE_UNCOMPILED --rename DEBUG $SOURCES")

# STYLESHEET(RELEASE)
env.Command([env['OUTPUT_STYLESHEET_RELEASE'], env['OUTPUT_STYLESHEET_RELEASE_MAP']], INPUT_STYLESHEET_FILES,
    STYLESHEET_COMMAND_COMMON + "--output-renaming-map-format CLOSURE_COMPILED --rename CLOSURE $SOURCES")


# TEMPLATE
import os
compiledSoys = []
for soy in INPUT_SOY_FILES:
  c = env.Command(os.path.join(env['OUTPUT_JAVASCRIPT_DIR'], os.path.basename(soy)) + ".js", soy,
    "$JAVA -jar $CLOSURE_TEMPLATE_JAR --shouldProvideRequireSoyNamespaces --cssHandlingScheme GOOG --outputPathFormat $TARGET $SOURCE")
  compiledSoys.append(c)


# DEPS
env.Command(env['OUTPUT_DEPS_JS'], INPUT_JAVASCRIPT_FILES + compiledSoys,
    build_command_string("$DEPSWRITER",
        "--root_with_prefix='%(item)s ../../../../%(item)s'",
        ["$OUTPUT_JAVASCRIPT_DIR", "$CLOSURE_TEMPLATE_DIR", "$INPUT_JAVASCRIPT_DIR"],
        "--output_file=$TARGET"))


COMPILER_INPUT_FILES = INPUT_JAVASCRIPT_FILES + compiledSoys + [env['OUTPUT_DEPS_JS']]
COMPILER_COMMAND_COMMON = build_command_string("$CLOSUREBUILDER", "--root=%(item)s",
    ["$INPUT_JAVASCRIPT_DIR", "$CLOSURE_LIBRARY_ROOT_DIR", "$CLOSURE_TEMPLATE_DIR", "$OUTPUT_JAVASCRIPT_DIR"],
    "--namespace=\"$NAMESPACE\" --compiler_jar=$CLOSURE_COMPILER_JAR")

# COMPILE(DEBUG)
env.Command(env['OUTPUT_JAVASCRIPT_DEBUG'], COMPILER_INPUT_FILES + [env['OUTPUT_STYLESHEET_DEBUG_MAP']],
    COMPILER_COMMAND_COMMON + \
    " --output_mode=script --compiler_flags=\"--js=$OUTPUT_STYLESHEET_DEBUG_MAP\" --output_file=$OUTPUT_JAVASCRIPT_DEBUG")

# COMPILE(RELEASE)
env.Command(env['OUTPUT_JAVASCRIPT_RELEASE'], COMPILER_INPUT_FILES + [env['OUTPUT_STYLESHEET_RELEASE_MAP']],
    COMPILER_COMMAND_COMMON + \
    " --output_mode=compiled --compiler_flags=\"--js=$OUTPUT_STYLESHEET_RELEASE_MAP\" " + \
    "--compiler_flags=\"--compilation_level=ADVANCED_OPTIMIZATIONS\" --output_file=$OUTPUT_JAVASCRIPT_RELEASE")
