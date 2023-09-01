# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Script to make adjustments to the Helios profile by adding in
# additional items by XML manipulation.  This should be more
# reliable than using diff-match-patch.
# There are still changes to be made after this script, but it is more
# efficient for these to be text substitutions.  These changes are not 
# committed.
# Arguments:
# 1. Filename for the original Helios Profile file
# 2. Filename for the Controls XML to be inserted into the profile 
# 3. Filename for the Bindings XML to be inserted into the profile 
# 4. Filename for the Interfaces XML to be inserted into the profile 
# 5. Filename of the resultant Helios profile
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import sys
import re
InputHeliosProfile = sys.argv[1]
hpfControlFileName = sys.argv[2]
hpfBindingFileName = sys.argv[3]
hpfInterfaceFileName = sys.argv[4]
OutputHeliosProfile = sys.argv[5]

print("Donor Helios Profile", InputHeliosProfile)
print("Control XML ", hpfControlFileName)
print("Binding XML ", hpfBindingFileName)
print("Interface XML ", hpfInterfaceFileName)
print("New Helios Profile ", OutputHeliosProfile)
print("Removing Embedded Viewports from ", InputHeliosProfile)

regex = r"(<EmbeddedViewportName>(.*)</EmbeddedViewportName>)"
subst = "<EmbeddedViewportName />"

import logging
logging.basicConfig(filename='ProxyLog.log', level=logging.INFO,format='%(asctime)s %(message)s')

with open(InputHeliosProfile, 'r') as f:
   # Read the file contents into a single variable
   contents = f.read()

logging.info('RegEx File Read: %s', InputHeliosProfile)

with open(InputHeliosProfile, 'w') as f:
     # actually write the lines
     f.write(re.sub(regex, subst, contents, 0, re.MULTILINE))

logging.info('RegEx File Write: %s', InputHeliosProfile)
	 
from defusedxml.ElementTree import parse
# parse the original input file
print("Reading existing profile XML: ",InputHeliosProfile)
et = parse(InputHeliosProfile)
root = et.getroot()

print("Reading additional controls XML: ",hpfControlFileName)
controlsRoot = parse(hpfControlFileName).getroot()

# Insert the additional Children at the start of the binding list 
for el in root:
    if el.tag == "Monitors":
        elm = el.find('Monitor')
        elc = elm.find('Children')
        i = 0
        for mel in controlsRoot:
            elc.insert(i,mel)
            i += 1
            # print("Adding Control for ", mel.find("StaticValue").text)
        continue

print("Reading additional binding XML: ",hpfBindingFileName)
bindingsRoot = parse(hpfBindingFileName).getroot()

# Insert the additional bindings at the start of the binding list 
for el in root:
    if el.tag == "Bindings":
        i = 0
        for mel in bindingsRoot:
            el.insert(i,mel)
            i += 1
            # print("Adding Binding for ", mel.find("StaticValue").text)
        continue
print("Reading additional interface XML: ",hpfInterfaceFileName)
interfacesRoot = parse(hpfInterfaceFileName).getroot()

# Insert the additional interfaces at the start of the interfaces list 
for el in root:
    if el.tag == "Interfaces":
        i = 0
        for mel in interfacesRoot:
            el.insert(i,mel)
            i += 1
            # print("Adding Interface for ", mel.find("StaticValue").text)
        continue

print("Writing new profile: ",OutputHeliosProfile)
et.write(OutputHeliosProfile,encoding="UTF-8",xml_declaration=True)

