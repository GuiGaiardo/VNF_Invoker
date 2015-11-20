#!/usr/bin/env python3.4
"""VNF Instanciation using Popen.

Can instanciate a valid ClickOS VM.
Can run a valid Click Script over
an already running ClickOS VM.
Can help configure a ClickOS VM cfg file.


Usage:
	Type a valid option:
		new-vm		#To instanciate a new ClickOS VM
		make-cfg	#To make a basic clickOS VM .cfg file
		select-vm	#To select a running ClickOS VM to work with
		run-script	#To set a ClickOS Script to run on the
					 selected VM
"""

import subprocess


global cosmos_path


def print_help():
	print("Usage:")
	print("    Type a valid option:")
	print("        new-vm      #To instanciate a new ClickOS VM")
	print("        make-cfg    #To make a basic clickOS VM .cfg file")
	print("        select-vm   #To select a running ClickOS VM to work with")
	print("        run-script  #To set a ClickOS Script to run on the")
	print("                     selected VM")


def get_cosmos_path():
	global cosmos_path
	cosmos_path = input("\n\nInsert the Cosmos executable absolute path.\n")


def get_bridge_name(cfg_path):
	bridge_name = ""
	with open(cfg_path, 'r') as cfg_file:
		for line in cfg_file:
			if "vif" in line and not ("#vif" in line):	#makes sure not to get a commented line
				str_start = line.find("bridge=") + len("bridge=")
				str_end = line[str_start:].find("'") + str_start
				bridge_name = line[str_start : str_end]
	
	return bridge_name


def create_bridge(bridge_name):
	return subprocess.call("sudo brctl addbr " + bridge_name, shell = True)


def boot_vm(cfg_path):
	return subprocess.call(cosmos_path + " create " + cfg_path, shell = True)


def new_vm():
	"""Instanciate a new ClickOS VM."""
	cfg_path = input("\n\nInsert the ClickOS .cfg file absolute path:\n")

	bridge_name = get_bridge_name(cfg_path)
	if len(bridge_name) == 0:
		print("Couldnt find the bridge name.")
		return 0

	create_bridge(bridge_name)

	boot_vm(cfg_path)

	return 1



def treat_command(command):
	if command == 'help':
		print_help()
		return 1
	if command == 'exit':
		print("Bye!\n\n")
		return 0
	if command == 'make-cfg':
		return make_cfg_file()
	
	if not len(cosmos_path):
		get_cosmos_path()

	if command == 'new-vm':
		return new_vm()



cosmos_path = ""

"""If treat_command() returns 0, then its 'exit' or error"""
while True:
	command = input("\n\nType 'help' if you dont know what to do or 'exit' to leave.\n")
	if not treat_command(command):
		break