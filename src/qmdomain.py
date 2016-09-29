#! /usr/bin/env python

# This module was written with the help of information here:
# http://samprocter.com/2014/06/documenting-a-language-using-a-custom-sphinx-domain-and-pygments-lexer/

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.roles import XRefRole
from sphinx.util.docfields import GroupedField
from sphinx.util.nodes import make_refnode

class DefinedObject(object):
    
    domain_str = ""
    
    def __init__(self, parent=None, docname=None, name="", title=None):
        self.parent = parent
        self.docname = docname
        self.name = name
        self.title = title

    def _get_untyped_id(self):
        if self.parent:
            return "%s.%s" % (self.parent._get_untyped_id(), self.name)
        else:
            return self.name
        
    def get_target_id(self):
        """Return a unique target name for a link"""
        if self.parent:
            return "%s.%s.%s" % (
                self.domain_str, self.parent._get_untyped_id(), self.name)
        else:
            return "%s.%s" % (self.domain_str, self.name)


class ODataService(DefinedObject):    
    domain_str = "od-service"


class ODataFeed(DefinedObject):    
    domain_str = "od-feed"


class ODataType(DefinedObject):
    domain_str = "od-type"


class ODataProperty(DefinedObject):
    domain_str = "od-prop"


class ODataServiceDirective(ObjectDescription):
    
    has_content = False
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    
    option_spec = {
        }
    
    def run(self):
        env = self.state.document.settings.env
        name = self.arguments[0].strip()
        obj = env.domaindata['od']['services'].get(name, None)
        if len(self.arguments) > 1:
            title = self.arguments[1].strip()
            if obj is None:
                obj = ODataService(name=name, title=title, docname=env.docname)
                env.domaindata['od']['objects'][obj.get_target_id()] = obj
            else:
                # set the title and the target document
                obj.title = title
                obj.docname = env.docname
            ret = []
            targetnode = nodes.target('', '', ids=[obj.get_target_id()])
            self.state.document.note_explicit_target(targetnode)
            ret.append(targetnode)
            ret.append(addnodes.desc_name(title, title))
            indextext = '%s (OData service)' % title
            inode = addnodes.index(
                entries=[('single', indextext, obj.get_target_id(), '')])
            ret.append(inode)
        else:
            if obj is None:
                # fill other attributes later as this isn't the definition
                obj = ODataService(name=name)
                env.domaindata['od']['services'][obj.get_target_id()] = obj
            ret = []
        # this service becomes the parental context
        env.temp_data['od:service'] = obj
        return ret


class ODataFeedDirective(ObjectDescription):

    option_spec = {
        'mle': directives.flag,
        }

    doc_field_types = [
        GroupedField('httpmethod', label='Methods Supported',
                     names=('method', )),
        GroupedField('filter', label='Filters supported',
                     names=('filter', )),
        GroupedField('expand', label='Expansions supported',
                     names=('expand', )),
        ]
    
    def handle_signature(self, sig, signode):
        """Format: <name> <entity-type>"""
        svc = self.env.temp_data.get('od:service', None)
        sig = sig.strip().split()
        fname = sig[0]
        ftype = sig[1]
        obj = ODataFeed(parent=svc, docname=self.env.docname,
                        name=fname, title=fname)
        tobj = ODataType(parent=svc, docname=self.env.docname, name=ftype,
                         title=ftype)
        signode += addnodes.desc_name(fname, fname)
        signode += nodes.Text(" ")
        signode += addnodes.pending_xref(
            ftype, nodes.Text(ftype), refdomain="od",
            reftype="type", reftarget=tobj._get_untyped_id())
        if 'mle' in self.options:
            signode += nodes.Text(" (Media Link Entry)")
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['od']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        self.indexnode['entries'].append(
            ('single', '%s (OData feed)' % name.title, targetname, ''))          


class ODataTypeDirective(ObjectDescription):
    
    def before_content(self):
        self.env.temp_data['od:type'] = self.names[0]
    
    def after_content(self):
        self.env.temp_data['od:type'] = None

    def handle_signature(self, sig, signode):
        """Format: just the name of the entity type itself"""
        svc = self.env.temp_data.get('od:service', None)
        name = sig.strip()
        obj = ODataType(parent=svc, docname=self.env.docname, name=name,
                        title=name)
        signode += addnodes.desc_annotation("EntityType: ", "EntityType: ")
        signode += addnodes.desc_name(name, name)
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['od']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        self.indexnode['entries'].append(
            ('single', '%s (OData entity type)' % name.title, targetname, ''))          


class ODataPropertyDirective(ObjectDescription):

    option_spec = {
        'key': directives.flag,
        'notnull': directives.flag,
        'collection': directives.flag,
        }

    def handle_signature(self, sig, signode):
        """Format: <name> <type>"""
        etype = self.env.temp_data['od:type']
        svc = self.env.temp_data.get('od:service', None)
        sig = sig.strip().split()
        pname = sig[0]
        ptype = sig[1]
        obj = ODataProperty(parent=etype, docname=self.env.docname,
                            name=pname, title=pname)
        tobj = ODataType(parent=svc, docname=self.env.docname, name=ptype,
                         title=ptype)
        if 'key' in self.options:
            signode += addnodes.desc_annotation("Entity Key: ", "Entity Key: ")
        signode += addnodes.desc_name(pname, pname)
        signode += nodes.Text(" ")
        if ptype.lower().startswith("edm."):
            signode += nodes.Text(" " + ptype)
        else:
            signode += addnodes.pending_xref(
                ptype, nodes.Text(ptype), refdomain="od",
                reftype="type", reftarget=tobj._get_untyped_id())
        if 'notnull' in self.options:
            signode += nodes.Text(" NOT NULL")
        if 'collection' in self.options:
            signode += nodes.Text(" Collection")
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['od']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        etype = name.parent
        if etype:
            self.indexnode['entries'].append(
                ('single', '%s (property of %s)' % (name.title, etype.title),
                targetname, ''))          
        else:
            self.indexnode['entries'].append(
                ('single', '%s (property of ?)' % name.title, targetname, ''))          
    

class ODataFeedRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        svc = env.temp_data.get('od:service', None)
        if svc is not None:
            # does target need qualifying?
            starget = target.split('.')
            if len(starget) < 2:
                target = svc.name + '.' + target
        return title, target


class ODataTypeRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        svc = env.temp_data.get('od:service', None)
        starget = target.split('.')
        if len(starget) < 2:
            # qualify with svc name
            if svc is not None:
                target = "%s.%s" % (svc.name, target)
        return title, target


class ODataPropRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        svc = env.temp_data.get('od:service', None)
        typ = env.temp_data.get('od:type', None)
        starget = target.split('.')
        if len(starget) < 2:
            # qualify with svc and type name
            if typ is not None:
                target = "%s.%s" % (typ.name, target)
                if svc is not None:
                    target = "%s.%s" % (svc.name, target)
        elif len(starget) < 3:
            # just the svc name
            if svc is not None:
                target = "%s.%s" % (svc.name, target)
        return title, target


class ODataDomain(Domain):
    """OData API domain"""
    name = 'od'
    label = 'OData'
    
    object_types = {
        'service':      ObjType('service', 'svc'),
        'feed':         ObjType('feed', 'feed'),
        'type':         ObjType('type', 'type'),
        'prop':         ObjType('prop', 'prop'),
        }

    directives = {
        'service': ODataServiceDirective,
        'feed': ODataFeedDirective,
        'type': ODataTypeDirective,
        'prop': ODataPropertyDirective,
        }
    
    roles = {
        'svc': XRefRole(),
        'feed': ODataFeedRole(),
        'type': ODataTypeRole(),
        'prop': ODataPropRole(),
        }

    initial_data = {
        'objects': {},  # target_name -> DefinedObject instance
        'services': {}, # service name -> ODataService instance
    }
    
    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        prefix = {
            'svc': 'od-service',
            'feed': 'od-feed',
            'type': 'od-type',
            'prop': 'od-prop',
            }.get(typ, None)
        if not prefix:
            return None
        qtarget = "%s.%s" % (prefix, target)
        objects = self.data['objects']
        obj = objects.get(qtarget, None)
        # TODO: add some context from the environment to support links
        # that happen within a service or type definition
        if obj is None:
            obj = objects.get(qtarget.lower(), None)
        if obj is not None:
            return make_refnode(builder, fromdocname, obj.docname,
                                obj.get_target_id(), contnode,
                                obj.title)
        else:            
            print qtarget
            return None


class SQLDatabase(DefinedObject):
    domain_str = "qm-db"
    
    
class SQLTable(DefinedObject):
    domain_str = "qm-table"
    

class SQLField(DefinedObject):
    domain_str = "qm-field"
    

class SQLTableDirective(ObjectDescription):
    
    def before_content(self):
        self.env.temp_data['qm:table'] = self.names[0]
    
    def after_content(self):
        self.env.temp_data['qm:table'] = None

    def handle_signature(self, sig, signode):
        """Format: just the name of the table itself"""
        name = sig.strip()
        obj = SQLTable(docname=self.env.docname, name=name.lower(), title=name)
        signode += addnodes.desc_annotation("TABLE ", "TABLE ")
        signode += addnodes.desc_name(name, name)
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['qm']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        self.indexnode['entries'].append(
            ('single', '%s (table in data model)' % name.title, targetname, ''))          


class SQLFieldDirective(ObjectDescription):

    option_spec = {
        'key': directives.flag,
        'notnull': directives.flag,
        'computed': directives.flag,
        }

    def handle_signature(self, sig, signode):
        """Format: <name> <type>"""
        table = self.env.temp_data['qm:table']
        sig = sig.strip().split()
        cname = sig[0]
        ctype = sig[1]
        obj = SQLField(parent=table, docname=self.env.docname,
                       name=cname.lower(), title=cname)
        if 'key' in self.options:
            signode += addnodes.desc_annotation("Primary Key: ",
                                                "Primary Key: ")
        signode += addnodes.desc_name(cname, cname)
        signode += nodes.Text(" ")
        signode += addnodes.desc_type(ctype, ctype)
        if 'computed' in self.options:
            signode += addnodes.desc_annotation(" computed", " computed")
        if 'notnull' in self.options:
            signode += nodes.Text(" NOT NULL")
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['qm']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        table = name.parent
        if table:
            self.indexnode['entries'].append(
                ('single', '%s (field in %s)' % (name.title, table.title),
                targetname, ''))          
        else:
            self.indexnode['entries'].append(
                ('single', '%s (database field)' % name.title, targetname, ''))          
    

class SOAPType(DefinedObject):
    domain_str = "qm-xtype"
    

class SOAPTypeDirective(ObjectDescription):
    
    option_spec = {
        'simple': directives.flag,
        }

    def before_content(self):
        self.env.temp_data['qm:xtype'] = self.names[0]
    
    def after_content(self):
        self.env.temp_data['qm:xtype'] = None

    def handle_signature(self, sig, signode):
        """Format: just the name of the type itself"""
        sig = sig.strip().split()
        name = sig[0]
        if len(sig) > 1:
            base = sig[1]
        else:
            base = None
        obj = SOAPType(docname=self.env.docname, name=name, title=name)
        if 'simple' in self.options:
            signode += addnodes.desc_annotation("simpleType ", "simpleType ")
        else:
            signode += addnodes.desc_annotation("complexType ", "complexType ")
        signode += addnodes.desc_name(name, name)
        if base:
            signode += nodes.Text(" extends ")
            signode += addnodes.pending_xref(
                base, nodes.Text(base), refdomain="qm",
                reftype="xtype", reftarget=base)            
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['qm']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        self.indexnode['entries'].append(
            ('single', '%s (SOAP type)' % name.title, targetname, ''))          


class SOAPField(DefinedObject):
    domain_str = "qm-xfield"
    

class SOAPFieldDirective(ObjectDescription):

    option_spec = {
        'optional': directives.flag,
        'max': lambda x:x,
        'default': lambda x: x
        }

    def handle_signature(self, sig, signode):
        """Format: <name> <type>"""
        xtype = self.env.temp_data['qm:xtype']
        sig = sig.strip().split()
        fname = sig[0]
        ftype = sig[1]
        obj = SOAPField(parent=xtype, docname=self.env.docname,
                        name=fname, title=fname)
        signode += addnodes.desc_name(fname, fname)
        signode += nodes.Text(" ")
        signode += addnodes.pending_xref(
            ftype, nodes.Text(ftype), refdomain="qm",
            reftype="xtype", reftarget=ftype)
        if 'max' in self.options:
            max_repeat = self.options['max'].strip().lower()
            if max_repeat == "unbounded":
                max_occurrs = " %s" % max_repeat
            else:
                max_repeat = int(max_repeat)
                if max_repeat > 1:
                    max_occurrs = " maxOccurs=%i" % max_repeat
                else:
                    max_occurrs = ""
            if max_occurrs:
                signode += addnodes.desc_annotation(max_occurrs, max_occurrs)
        if 'default' in self.options:
            default = self.options['default'].strip()
            default = " default=%s" % default
            signode += addnodes.desc_annotation(default, default)
        if 'optional' in self.options:
            signode += addnodes.desc_annotation(" optional", " optional")
        else:
            signode += addnodes.desc_annotation(" required", " required")
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['qm']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        xtype = name.parent
        if xtype:
            self.indexnode['entries'].append(
                ('single', '%s (element in %s)' % (name.title, xtype.title),
                targetname, ''))          
        else:
            self.indexnode['entries'].append(
                ('single', '%s (element)' % name.title, targetname, ''))          


class SOAPMethod(DefinedObject):
    domain_str = "qm-meth"
    

class SOAPMethodDirective(ObjectDescription):
    
    option_spec = {
        'input': lambda x: x,
        'output': lambda x: x,
        }

    def handle_signature(self, sig, signode):
        """Format: just the name of the method itself"""
        name = sig.strip()
        obj = SOAPMethod(docname=self.env.docname, name=name, title=name)
        signode += addnodes.desc_annotation("method ", "method ")
        signode += addnodes.desc_name(name, name)
        signode += nodes.Text(" (")
        if 'input' in self.options:
            comma = False
            for input in self.options['input'].split(','):
                pname, input_type = input.split()
                if comma:
                    signode += nodes.Text(", %s " % pname)
                else:
                    signode += nodes.Text("%s " % pname)
                    comma = True
                signode += addnodes.pending_xref(
                    input_type, nodes.Text(input_type), refdomain="qm",
                    reftype="xtype", reftarget=input_type)                    
        signode += nodes.Text(")")
        if 'output' in self.options:
            pname, output_type = self.options['output'].split()
            signode += nodes.Text(" returns ")
            signode += addnodes.pending_xref(
                output_type, nodes.Text(output_type), refdomain="qm",
                reftype="xtype", reftarget=output_type)
            signode += nodes.Text(" ")
        return obj
    
    def add_target_and_index(self, name, sig, signode):
        targetname = name.get_target_id()
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        objects = self.env.domaindata['qm']['objects']
        if targetname in objects:
            self.warning("duplicate object description: %s" % targetname)
        objects[targetname] = name
        self.indexnode['entries'].append(
            ('single', '%s (SOAP method)' % name.title, targetname, ''))          


class QMDomain(Domain):
    """Questionmark API domain."""
    name = 'qm'
    label = 'Questionmark'

    object_types = {
        'db':       ObjType('db', 'db'),
        'table':    ObjType('table', 'table'),
        'field':    ObjType('field', 'field'),
        'meth':     ObjType('meth', 'meth'),
        'xtype':    ObjType('xtype', 'xtype'),
        'xfield':   ObjType('xfield', 'xfield'),
        }
    
    directives = {
        'table': SQLTableDirective,
        'field': SQLFieldDirective,
        'meth': SOAPMethodDirective,
        'xtype': SOAPTypeDirective,
        'xfield': SOAPFieldDirective,
        }
    
    roles = {
        'table': XRefRole(),
        'field': XRefRole(),
        'xfield': XRefRole(),
        'xtype': XRefRole(),
        'meth': XRefRole(),
        }

    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }
    
    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        prefix = {
            'db': 'qm-db',
            'table': 'qm-table',
            'field': 'qm-field',
            'meth': 'qm-meth',
            'xfield': 'qm-xfield',
            'xtype': 'qm-xtype',
            }.get(typ, None)
        if not prefix:
            return None
        objects = self.env.domaindata['qm']['objects']
        qtarget = "%s.%s" % (prefix, target)
        target_obj = objects.get(qtarget, None)
        if target_obj is None:
            qtarget = "%s.%s" % (prefix, target.lower())
        target_obj = objects.get(qtarget, None)            
        if target_obj is not None:
            return make_refnode(builder, fromdocname, target_obj.docname,
                                qtarget, contnode, target_obj.title)
        else:            
            print qtarget
            return None

