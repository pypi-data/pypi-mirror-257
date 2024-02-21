from dataclasses import dataclass

from cocas.object_module import CodeLocation, ObjectModule

from .ast_nodes import InstructionNode, LabelDeclarationNode, ProgramNode, TemplateSectionNode
from .code_block import Section
from .exceptions import AssemblerException, AssemblerExceptionTag
from .targets import IVaryingLengthSegment, TargetInstructions


@dataclass
class Template:
    def __init__(self, sn: TemplateSectionNode, target_instructions: TargetInstructions):
        self.name: str = sn.name
        self.labels: dict[str, int] = dict()

        size = 0
        temp_storage = dict()
        for line in sn.lines:
            if isinstance(line, LabelDeclarationNode):
                label_name = line.label.name
                if label_name in self.labels:
                    raise AssemblerException(AssemblerExceptionTag.TPLATE, line.location.file, line.location.line,
                                             f'Duplicate label "{label_name}" declaration')
                if line.external:
                    raise AssemblerException(AssemblerExceptionTag.TPLATE, line.location.file, line.location.line,
                                             'External labels not allowed in templates')
                elif line.entry:
                    raise AssemblerException(AssemblerExceptionTag.TPLATE, line.location.file, line.location.line,
                                             'Ents not allowed in templates')
                else:
                    self.labels[label_name] = size

            elif isinstance(line, InstructionNode):
                if line.mnemonic not in target_instructions.assembly_directives():
                    raise AssemblerException(AssemblerExceptionTag.TPLATE, line.location.file, line.location.line,
                                             'Only these directives allowed in templates: ' +
                                             ', '.join(target_instructions.assembly_directives()))
                for seg in target_instructions.assemble_instruction(line, temp_storage):
                    size += seg.size

        self.labels['_'] = size


def gather_local_labels(sects: list[Section]):
    local_labels = dict()
    for sect in sects:
        local_labels.update({p for p in sect.labels.items() if not p[0].startswith('$')})
    return local_labels


@dataclass
class VaryingLengthEntry:
    seg: IVaryingLengthSegment
    sect: Section
    pos: int
    location: CodeLocation


def update_varying_length(sections: list[Section], known_labels: dict[str, int],
                          template_fields: dict[str, dict[str, int]]):
    labels = gather_local_labels(sections)
    labels.update(known_labels)
    var_len_entries: list[VaryingLengthEntry] = []
    for sect in sections:
        pos = sect.address
        for seg in sect.segments:
            if isinstance(seg, IVaryingLengthSegment):
                a = VaryingLengthEntry(seg, sect, pos, seg.location)
                var_len_entries.append(a)
            pos += seg.size

    changed = True
    while changed:
        changed = False
        for vl in var_len_entries:
            shift = vl.seg.update_varying_length(vl.pos, vl.sect, labels, template_fields)
            if shift:
                for other_vl in var_len_entries:
                    if other_vl.sect is vl.sect and other_vl.pos > vl.pos:
                        other_vl.pos += shift
                changed = True


def generate_object_module(pn: ProgramNode, target_instructions: TargetInstructions) -> ObjectModule:
    templates = [Template(t, target_instructions) for t in pn.template_sections]
    template_fields = dict([(t.name, t.labels) for t in templates])

    asects = [Section(asect, target_instructions) for asect in pn.absolute_sections]
    rsects = [Section(rsect, target_instructions) for rsect in pn.relocatable_sections]
    asects.sort(key=lambda s: s.address)

    update_varying_length(asects, {}, template_fields)
    asects_labels = gather_local_labels(asects)
    for rsect in rsects:
        update_varying_length([rsect], asects_labels, template_fields)

    obj = ObjectModule([asect.to_object_section_record(asects_labels, template_fields) for asect in asects],
                       [rsect.to_object_section_record(asects_labels, template_fields) for rsect in rsects])
    return obj
