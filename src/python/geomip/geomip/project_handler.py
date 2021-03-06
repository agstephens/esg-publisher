"""-*- Python -*-
Project handler template.

To create a project handler:

    - Fill in the methods in CustomProjectHandler. See the documentation
      for ProjectHandler class. At a minimum, readContext must be implemented.
      Note: The handler class name is arbitrary, provided it matches
      the setup.py 'handler' entry point of the esgcet.project_handlers group.
      
    - Install the handler package:

        python setup.py --verbose install
        
    - In esg.ini, associate the project and handler name, e.g.:

        [project:my_project]
        ...
        project_handler = <project_handler_name>
"""
from esgcet.exceptions import *
from esgcet.config import IPCC5Handler


class CustomProjectHandler(IPCC5Handler):

    def validateFile(self, fileobj):
        """Raise ESGInvalidMetadataFormat if the file cannot be processed by this handler."""
        if not fileobj.hasAttribute('project_id'):
            result = False
            message = "No global attribute: project_id"
        else:
            project_id = fileobj.getAttribute('project_id', None)
            result =  (project_id[:5]=="GeoMIP")
            message = "project_id should be 'GeoMIP'"
        if not result:
            raise ESGInvalidMetadataFormat(message)

    # No-op for GeoMIP
    def generateDerivedContext(self):
        pass

    def getContext(self, **context):
        """
        Read all metadata fields from the file associated with the handler. Typically this is the first file
        encountered in processing. The assumption is that all files contain the global metadata
        to be associated with the project. The file path is in self.path, and may be changed if necessary.

        Calls ``readContext`` to read the file.

        Returns a context dictionary of fields discovered in the file.

        context
          Dictionary of initial field values, keyed on field names. If a field is initialized, it is not overwritten.
        """
        # If the first processed file does not contain the correct metadata,
        # reset self.path to the correct path
        #
        #   self.path = the_correct_metadata_file_path
        #   
        # Call readContext to read the metadata into self.context
        IPCC5Handler.getContext(self, **context)

        # Add attribute/value pairs not contained in the file. For example,
        # to add an attribute 'creation_time' whose value is the current time (string):
        #
        # if self.context.get('creation_time', '')=='':
        #     self.context['creation_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Return the context dictionary
        return self.context

    def readContext(self, fileInstance, **kw):
        """Get a dictionary of attribute/value pairs from an open file.

        Returns a dictionary of attribute/value pairs, which are added to the handler context.

        fileInstance
          Format handler instance representing the opened file, an instance of FormatHandler
          or a subclass.

        kw
          Optional keyword arguments.

        """
        result = IPCC5Handler.readContext(self, fileInstance, **kw)

        # Extract the project-related metadata from file.
        # For example, if fileInstance is an instance of esgcet.config.CdunifFormatHandler,
        # to read the 'title' attribute from the file:
        #
        # f = fileInstance.file
        # if hasattr(f, 'title'):
        #     result['title'] = f.title

        # Return the attribute/value dictionary
        return result
