FROM arm32v7/python:3.6

WORKDIR /gpio_database_generator

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /gpio_database_generator/requirements.txt
RUN pip install -r requirements.txt

# Now copy in our code, and run it
COPY . /gpio_database_generator
#zum entwickeln
#CMD tail -F /dev/null
#ausführen
 CMD python /gpio_database_generator/gpio_database_generator.py