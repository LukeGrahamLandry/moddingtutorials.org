generated_redirects = []

unversioned = ["solutions", "intro", "dependencies", "java-basics", "publishing", "m1", "mixins"]
pages = ["advanced-blocks", "advanced-items", "arrows", "basic-blocks", "basic-items", "enchantments", "environment-setup", "recipes", "tile-entities", "tools-armor", "updating", "world-gen"]
concepts = ["sides", "registries", "mappings", "events"]
def process(old_version, new_version):
    for page in pages:
        generated_redirects.append("{0}/{2} /{1}/{2}".format(old_version, new_version, page))
    
    generated_redirects.append("{0}/topics /".format(old_version))
    if old_version != "":
        generated_redirects.append("{0} /{1}".format(old_version, new_version))
        
        for page in unversioned:
            generated_redirects.append("{0}/{2} /{2}".format(old_version, new_version, page))
    
    for page in concepts:
        generated_redirects.append("{0}/{2} /concepts#{2}".format(old_version, new_version, page))

process("", "1.19.2")  # change to 1.19.3
process("/o19", "1.19.2")
process("/o18", "1.18.2")
process("/o16", "1.16.5")
process("/o17", "1.18.2")

lines = []
with open("static/_redirects", "r") as f:
    manual_redirects = f.read()

manual_redirects = manual_redirects.split("# Generated\n")
lines = manual_redirects[0].split("\n") + ["# Generated"] + generated_redirects + ["# Generated"] + manual_redirects[2].split("\n")

with open("static/_redirects", "w") as f:
    f.writelines(s + "\n" for s in lines if s != "")
