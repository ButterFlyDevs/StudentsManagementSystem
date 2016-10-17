from fabric.api import run
from fabric.api import local # to run local comands
from fabric.colors import red
from provisioner import example_data_provisioner

##########################
#  FABRIC Fabfile.
# This is the file to configure Fabric Python Library to admin tasks

# Use:
# fab <commands>

# How to know the commands? :
# fab -l

##########################

SMS_Back_End_default_port = '8001' # api gateway microservice default port
SMS_Back_End_default_admin_port = '8083'

SMS_Front_End_default_port = '8080'  # Web default port
SMS_Front_End_default_admin_port = '8082'


def run_back_end():
    """
    Running SMS Back-End
    """
    print (red('### Running SMS Back-End in localhost in background. ###'))
    print (red('Please look at the list below to know the microservices ports.'))
    print (red('Note that default is apigms microservice.'))

    local('google_appengine/dev_appserver.py '
          ' --port=' + SMS_Back_End_default_port +
          ' --admin_port=' + SMS_Back_End_default_admin_port +
          ' SMS-Back-End/apigms/apigms.yaml '
          'SMS-Back-End/dbms/dbms.yaml '
          'SMS-Back-End/sce/sce.yaml &')

    print (red('Thanks for your contribution!'))


def run_dbms_api_test():
    """
    Run dbms api test
    """
    local('pytest -s SMS-Back-End/dbms/test')

def run_apigms_api_test():
    """
    Run apigms api test
    """
    local('pytest -s SMS-Back-End/apigms/test')

def run_front_end():
    """
    Run SMS Front-End in local.
    """
    print (red('### Running SMS Front-End in localhost in background. ###'))
    print (red('Please look at the list below to know the microservice ports.'))

    local('google_appengine/dev_appserver.py '
          ' --port=' + SMS_Front_End_default_port +
          ' --admin_port=' + SMS_Front_End_default_admin_port +
          ' SMS-Front-End/app.yaml &')

    print (red('Thanks for your contribution!'))


def run_mysql():
    """
    Start mysql daemon.
    """
    print (red('### Running MySQL daemon. ###'))
    local('sudo /etc/init.d/mysql start')


def data_provision():
    print (red('### Provisioning example data to system. ###'))
    example_data_provisioner.run()


def run_all():
    """
    Run entire project, included MySQL daemon, SMS Front-End dev_server and Back-End dev_server.
    """
    run_mysql()  # Run database engine
    run_back_end()  # Run all microservices in Back End
    run_front_end()  # Run Front End
    data_provision()  # Fill the system with example data.

def kill_all():
    """
    Kill all processes that is related with google dev servers.
    """
    print (red("Kill all processes that are related with google dev server."))
    local("kill -9 $(ps -aux | grep google | awk '{ print $2 }' | head -n -1)")

