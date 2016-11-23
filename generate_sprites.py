import pefile
from PIL import Image
from io import BytesIO

pe = pefile.PE('SkypeResources.dll')

image = Image.new("RGBA", (20, 20), (0, 0, 0, 255))
image.save('sprites/empty.png')

css_file = open('skype_sprites.css', 'w+')
css_template = """
.{name} {{
    height: 0;
    width: 0;
    padding: {padding}px {padding}px;
    background-repeat: no-repeat;
    background: url('sprites/{name}.png') left top;
    background-size: cover;
    animation: play_{name} {duration}s steps({steps}) infinite;
}}
@keyframes play_{name} {{
    100% {{ background-position: 0px {y_position}px; }}
}}
"""

html_template_start = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title></title>
        <link rel="stylesheet" href="skype_sprites.css" media="screen" title="no title">
    </head>
    <body>
"""
html_template_insert = """
        <div>
            <h3>.{name}</h3>
            <img src="sprites/empty.png" class="{name}">
        </div>
"""
html_template_end = """
    </body>
</html>
"""
html_file = open('example.html', 'w+')
html_file.write(html_template_start)

counter = 0
for rt_string_directory in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    for i, entry in enumerate(rt_string_directory.directory.entries):
        data_rva = entry.directory.entries[0].data.struct.OffsetToData
        size = entry.directory.entries[0].data.struct.Size

        data = pe.get_memory_mapped_image()[data_rva:data_rva + size]
        if data[1:4].decode('utf-8', errors='replace') == 'PNG':
            image = Image.open(BytesIO(data))
            with Image.open(BytesIO(data)) as image:
                if image.height % image.width == 0:
                    if image.height // image.width > 6:
                        print('processing entry #', i, end='\r')
                        name = 'entry_' + str(i)
                        with open('sprites/'+name+'.png', 'wb+') as f:
                            f.write(data)
                        steps = image.height // image.width
                        padding = image.width // 2
                        # 20 fps
                        duration = format(steps * 0.05, '.2f')
                        y_position = image.height * -1
                        styles = css_template.format(name=name, padding=padding,
                                                     duration=duration,
                                                     steps=steps,
                                                     y_position=y_position)
                        css_file.write(styles)
                        html_insert = html_template_insert.format(name=name)
                        html_file.write(html_insert)
                        counter += 1
css_file.close()
html_file.write(html_template_end)
html_file.close()
print()
print('done', counter, 'entrie(s)')
