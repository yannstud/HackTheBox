require 'winrm'

conn = WinRM::Connection.new(
	endpoint: 'http://10.10.10.169:5985/wsman',
  user: 'melanie',
  password: 'Welcome123!',
)

command=""

conn.shell(:powershell) do |shell|
    until command == "exit\n" do
        print "PS > "
        command = gets        
        output = shell.run(command) do |stdout, stderr|
            STDOUT.print stdout
            STDERR.print stderr
        end
    end    
    puts "Exiting with code #{output.exitcode}"
end
