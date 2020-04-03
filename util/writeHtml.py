"""
@author: cjing9017
@date: 2019/09/05
"""


class WriteHtml(object):

    def __init__(self, type_pattern, type_policy, type_map):
        super(WriteHtml, self).__init__()
        self.policy = type_policy
        self.map = type_map
        self.pattern = type_pattern

    def write_html(self):
        message = """
            <h2>Configuration Information</h2>
            <h4>Pattern</h4>
            <ul>
                <li>%s</li>
            </ul>
            <h4>Policy</h4>
            <ul>
                <li>%s</li>
            </ul>
            <h4>Map</h4>
            <ul>
                <li>%s</li>
            </ul>
        """ % (self.pattern, self.policy, self.map)
        with open("./../resource/html/configurationInformation.html", 'w') as f:
            f.write(message)
