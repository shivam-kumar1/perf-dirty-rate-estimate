import subprocess, time, sys

if len(sys.argv) != 2:
  print("Error: Expecting VM uuid as the (only) argument.")
  exit(-1)

dom = sys.argv[1]
cmd = "virsh qemu-monitor-command %s '{\"execute\": \"query-migrate\"}'" % dom
out_file = "migrate_stats"
output = open(out_file, "w")

dom_status = False

while True:

  proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()

  if err != '' and err.find(dom) != -1:
    if dom_status:
      print("Info: Domain %s migrated. Stats saved in '%s' file." % (dom, out_file))
    else:
      print("Error: Domain %s was not found on this host." % dom)
    break

  if out.find("completed") != -1:
    print("Error: No active migration for domain %s." % dom)
    break

  dom_status = True
  output.write(out)
  time.sleep(0.5)

output.close()
