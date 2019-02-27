# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import os
import Pyro4

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class DashboardSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(DashboardSkill, self).__init__(name="Dashboard")

        

    @intent_handler(IntentBuilder("").require("Open").require("Dashboard"))
    def handle_dashboard_control_itnent(self, message):
        with open("uri.txt", 'r') as myfile:
            uri = myfile.read()
        if uri.strip():
            self.speak_dialog("dashboard.already.active")
        else:
            os.system('/usr/bin/python3 ~/Desktop/RPiDashboard/main.py')
            #self.speak_dialog("active")

    @intent_handler(IntentBuilder("").require("Background").require("Colour"))
    def handle_change_background_colour_intent(self, message):
        with open("uri.txt", 'r') as myfile:
            uri = myfile.read()
        try:
            app = Pyro4.Proxy(uri)
            if message.data["Colour"] == "red":
                app.change_background_to_red()
            else:
                app.change_background_to_blue()
        except:
            print("Pyro could not create connection")
    
    @intent_handler(IntentBuilder("").require("Close").require("Dashboard"))        
    def close_dashboard_intent(self, message):
        with open("uri.txt", 'r') as myfile:
            uri = myfile.read()
        app = Pyro4.Proxy(uri)
        app.shutdown()
        app._pyroRelease()

    @intent_handler(IntentBuilder("").require("Reset").require("Dashboard"))        
    def reset_intent(self, message):
        text_file = open("uri.txt", "w")
        text_file.write("")
        text_file.close()   


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return DashboardSkill()
