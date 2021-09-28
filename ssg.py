import os
import yaml
from jinja2 import Template

resDir = "res/"
outDir = "www/"
inDir = "src/"

templateFn = "template.html"

def gen_single_page( template, pageFn ):
  # ingest pageFile
  with open( pageFn, "r" ) as pageFile:
    pageLines = pageFile.readlines()
  pContent = ''.join(pageLines)

  writeFn, pTitle = get_page_details( pageFn )

  # render
  if pContent != '':
    finalPage = template.render(content=pContent, title=pTitle)
  else:
    finalPage = template.render(title=pTitle)

  # write
  if not assert_fn( writeFn ):
    return False

  with open( writeFn, "w+" ) as writeFile:
    writeFile.write( finalPage )

def get_page_details( pageFn ):
  DEFAULT_WRITEFN = outDir + pageFn[len(inDir):]
  DEFAULT_TITLE = " - " + os.path.splitext(pageFn)[0]

  pageYmlFn = os.path.splitext(pageFn)[0] + ".yml"

  if os.path.isfile(pageYmlFn):
    with open( pageYmlFn, "r" ) as pageYmlFile:
      pageYml = yaml.safe_load( pageYmlFile )

    try:
      writeFn = outDir + pageYml["destination"]
    except:
      writeFn = DEFAULT_WRITEFN

    try:
      pTitle = pageYml["title"]
    except:
      pTitle = DEFAULT_TITLE

  else:
    writeFn = DEFAULT_WRITEFN
    pTitle = DEFAULT_TITLE

  return writeFn, pTitle
  

def assert_fn( filename ):
  if not os.path.isfile(filename):
    dirname = os.path.dirname(filename)
    if dirname != "":
      if not os.path.isdir( os.path.dirname(filename) ):
        if os.path.isabs( dirname ):
          print("  [-] Invalid fn, cannot be absolute: " + filename)
          return False
        os.makedirs(dirname)
  return True

def main():
  with open( templateFn, "r" ) as templateFile:
    template = Template( templateFile.read() )
    
  pages = [os.path.join(dp, f) for dp, dn, fn in os.walk(inDir) for f in fn]
  print(pages)
  
  for pageFn in pages:
    if os.path.splitext(pageFn)[1] == ".html":
      print("[+] Generating from: " + pageFn )
      gen_single_page( template, pageFn )

  # copy res into outdir
  os.system(f'cp -r {resDir}/* {outDir}')

if __name__ == "__main__":
  main()

