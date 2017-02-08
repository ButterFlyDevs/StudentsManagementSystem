from fabric.api import local  # to run local commands.
from fabric.colors import red
from provisioner import example_data_provisioner
import time
from fabric.api import local, lcd, run  # to run local commands.
from fabric.colors import red, blue
from provisioner import example_data_provisioner
import time

##########################
#  FABRIC Fabfile.  <http://www.fabfile.org/>
# This is the file to configure Fabric Python Library to admin tasks

# Use:
# fab <command>

# How to know the commands? :
# fab -l

# Info about command:
# fab -d <command>

##########################

SMS_Back_End_default_port = '8001'  # api gateway microservice default port
SMS_Back_End_default_admin_port = '8083'

SMS_Front_End_default_port = '8080'  # Web default port
SMS_Front_End_default_admin_port = '8082'


def run_back_end(ms=None):
    """
    Running SMS Back-End
    """

    # Run only scms (Students Control micro Service)
    if ms == 'scms':
        local('google_appengine/dev_appserver.py' +
              ' --port=8003 --host=0.0.0.0 --admin_port=8083 ' +
              'SMS-Back-End/scms/scms.yaml &')
        pass

    if ms == None:


        print (red('### Running SMS Back-End in localhost in background. ###'))
        print (red('Please look at the list below to know the microservices ports.'))
        print (red('Note that default is apigms microservice.'))

        local('google_appengine/dev_appserver.py'
              ' --port=' + SMS_Back_End_default_port +
              ' --host=0.0.0.0 --admin_port=' + SMS_Back_End_default_admin_port +
              ' SMS-Back-End/apigms/apigms.yaml '
              'SMS-Back-End/dbms/dbms.yaml '
              'SMS-Back-End/scms/scms.yaml &')

        print (red('Thanks for your contribution!'))


def test(ms):
    """
    Tests runner.
    Execute the test over specific microservice, part ot it of over all system.

    Example: fab test:'tdbms'

    If something fail maybe it could be the pythonpath system.
    export PYTHONPATH="${PYTHONPATH}:/home/.../StudentsManagementSystem/SMS-Back-End/dbms/dbapi"


    """
    # All [[ Teaching Data Base microService ]].
    if ms == 'tdbms':
        print (blue('## Runnig Teaching Daba Base microService entire Test Suite. ## '))
        print (blue('## Runnig Teaching Daba Base microService dbapi library test. ## '))
        with lcd("SMS-Back-End/dbms/dbapi"):
            local("pytest test/ -vv")
        print (blue('## Runnig Teaching Daba Base microService apiRest test. ## '))
        with lcd("SMS-Back-End/dbms"):
            local("pytest test/ -vv")

    # Only the apiRest.
    if ms == 'tdbms.api':
        print (blue('## Runnig Teaching Daba Base microService apiRest test. ## '))
        with lcd("SMS-Back-End/dbms"):
            local("pytest test/ -vv")

    # It fail yet:
    if ms == 'tdbms.dbapi':
        print (blue('## Runnig Teaching Daba Base microService dbapi library test. ## '))
        with lcd("SMS-Back-End/dbms/dbapi"):
            local("pytest test/ -vv")


    if ms == 'scms':
        print (blue('## Runnig Students Control microService entire Test Suite. ## '))
        with lcd("SMS-Back-End/scms"):
            local("pytest test/ -vv")


def doc(ms):
    """
    Doc generator.
    Build the documentation to the microservice passed.

    Examples:
        fab doc:'tdbms'
        fab doc:'apigms'
        fab doc:'back-end'
    """

    # Generate and open the documentation of Teaching DataBase microService
    if ms == 'tdbms':
        local('make -C SMS-Back-End/dbms/docs html')
        local('firefox SMS-Back-End/dbms/docs/build/html/index.html')

    if ms == 'scms':
        local('make -C SMS-Back-End/scms/docs html')
        local('firefox SMS-Back-End/scms/docs/build/html/index.html')

    if ms == 'apigms':
        local('make -C SMS-Back-End/apigms/docs html')
        local('firefox SMS-Back-End/apigms/docs/build/html/index.html')

    if ms == 'back-end':
        local('make -C SMS-Back-End/docs html')
        local('firefox SMS-Back-End/docs/build/html/index.html')


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
          ' --host=0.0.0.0 --admin_port=' + SMS_Front_End_default_admin_port +
          ' SMS-Front-End/app.yaml &')

    print (red('Thanks for your contribution!'))


def run_mysql():
    """
    Start mysql daemon.
    """
    print (red('### Running MySQL daemon. ###'))
    local('sudo /etc/init.d/mysql start')


def data_provision(kind='Simple'):
    """
    Run the data provisioning procedure using the APIGmS.

    fab data_provision:kind='Simple'
    """

    if kind in ['Comlex', 'complex', 'C']:
        example_data_provisioner.run()  # Fill the system with example data.
    if kind in ['Simple', 'simple', 'S']:
        print 'yeah'


def requirements(ms=None):
    """
    Install all requirements for all or for some microservice.

    Example of use:
        fab requirements:ms=dbms
        fab requirements # All system

    """

    def local_requirements():

        commands = [
            'apt-get install -y unzip',
            'apt-get install -y curl',
            'curl -O https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.30.zip',
            'unzip google_appengine_1.9.30.zip',
            'rm google_appengine_1.9.30.zip',
            'apt-get install -y python-pip',
            'pip install -r requirements.txt ',
        ]

        for command in commands:
            local(command)

    available_options = ['dbms', 'apigms', 'uims', 'local']
    if ms is not None:
        if ms in available_options:
            if ms == available_options[0] or ms == available_options[1]:
                path = 'SMS-Back-End/' + ms + '/'

                command = 'pip install -r ' + path + 'requirements.txt -t ' + path + 'lib/'
                local(command)

            if ms == 'uims':
                command = 'cd SMS-Front-End/app ; bower install'
                local(command)

            if ms == 'local':
                local_requirements()

        else:
            print ms + ' microservice doesn\'t exists.'
            print 'The avilable options are: ' + str(available_options)
            print 'Example of use: fab requirements:ms=dbms'
    else:

        print 'Requirements in entire project.'

        for a in range(0, 2):
            path = 'SMS-Back-End/' + available_options[a] + '/'
            command = 'pip install -r ' + path + 'requirements.txt -t ' + path + 'lib/'
            local(command)

        command = 'cd SMS-Front-End/app ; bower install'
        local(command)

        # Run local requirements.
        local_requirements()


def run(provision=False, kind='Simple'):
    """
    Run entire project, included MySQL daemon, SMS Front-End dev_server and Back-End dev_server.

    Example of use:
        fab run:provision=yes
    """

    run_mysql()  # Run database engine
    run_back_end()  # Run all microservices in Back End
    run_front_end()  # Run Front End
    time.sleep(5)

    if provision is True:
        data_provision(kind)


def kill():
    """
    Kill all processes that is related with google dev servers.
    """
    print (red("Kill all processes that are related with google dev server."))
    local("kill -9 $(ps -aux | grep google | awk '{ print $2 }' | head -n -1)")
