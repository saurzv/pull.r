import glob

def get_manual(embed):
        """ Get manual for every command """

        for file in glob.glob('./man/*'):
            filename = file.split('/')[2]
            with open(file, 'r') as f:
                line = f.read()
                embed.add_field(name=filename, value=line, inline=False)