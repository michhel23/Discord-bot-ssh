#python3
import discord #pip install discord
import paramiko #pip install paramiko
from io import BytesIO #pip install io


ip_address = #complete with an ip adresse (str)
username = #complete username (str)
password = #complete passwrd (str)
port = "22" #port for ssh connection (str)
Token= #complete with the bot token (str)
#start the ssh
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_address, port, username, password)


client = discord.Client()



def is_me(m):
    return m.author == client.user

def outputF(stderr,stdout):
    output=''
    line = stderr.readline()
    while line:
        output += str(line)
        line = stderr.readline()

    line2 = stdout.readline()
    while line2:
        output += str(line2)
        line2 = stdout.readline()

    return output


def addPath(name,Path):
    with open(name,'a') as f:
        print(f)
        cmd="cd "+str(Path)
        f.write(cmd)
    f.close()


@client.event
async def on_ready():
    print('ready!!')
    Path= #where you want to start the terminal (Path) > str
    with open("logbot.txt",'w') as f:
        f.write(Path)


@client.event
async def on_message(message):
    if str(message.channel) == 'terminal-linux' and message.author.bot!=True and message.content[0]!="/":
        await message.channel.send('```<[Processing...]>```')
        if "shutdown" in message.content:
            await message.channel.send('```<[Shut down machine]>```')
        cmd = message.content

        if "cd " in cmd :
            with open("logbot.txt") as f:
                Path=f.read()
            commande="cd "+ Path +" && "+cmd +" && pwd"
            stdin, stdout, stderr = ssh.exec_command(commande)
            output = outputF(stdout,stderr)
            print(output)
            if "no such file or directory" in output:
               print('fail')
            else:
               with open("logbot.txt",'w') as f:
                    f.write(output)
                    

            await message.channel.purge(limit=1, check=is_me)
            await message.channel.send("```\n┏━("+username+"@kali-rpi)-[-"+Path+"]\n┗━$ "+cmd+"\n"+output+"```")

        else:
            with open("logbot.txt") as f:
                Path=f.read()
                Path=Path.replace('\n','')
            commande="cd "+ Path +" && "+cmd
            stdin, stdout, stderr = ssh.exec_command(commande)
            output = outputF(stderr,stdout)
            await message.channel.purge(limit=1, check=is_me)
            if len(output)>=2000:
                await message.channel.send("```+ 2000 char```")
                buffer = BytesIO(output.encode('utf-8'))
                file = discord.File(buffer, filename='output.txt')
                await message.channel.send(file=file)
            else:
                await message.channel.send("```\n┏━("+username+"@kali-rpi)-[-"+Path+"]\n┗━$ "+cmd+"\n"+output+"```")





client.run(Token) #your bot token