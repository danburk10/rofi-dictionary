# models/dictionary_entry.py

#WordEntry that will be passed back from providers. used to standardize the output from different touchpoints (api,sqlite,json...)

from dataclasses import dataclass, field
from typing import List, Optional

#@dataclass
#class DictionaryEntry:
#    word: str
#    definition: str
#    part_of_speech: str | None = None
#    phonetic: str | None = None
#    example: str | None = None
#    synonyms: list[str] = field(default_factory=list)
#    source: str | None = None

@dataclass
class Definition:
    definition: Optional[str] = None
    part_of_speech: str = None
    examples: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    antonyms: list[str] = field(default_factory=list)

    def get_definition(self):
        return self.definition

@dataclass
class WordEntry:
    word: str
    phonetic: Optional[str] = None
    audio_url: Optional[str] = None
    definitions: list[Definition] = field(default_factory=list)
    origin: Optional[str] = None
    source: Optional[str] = None


    def add_definition(self, definition: str,
                       part_of_speech: str, 
                       examples: list[str],
                       synonyms: list[str],
                       antonyms: list[str],
                       **kwargs):
        self.definitions.append(Definition(definition, 
                                           part_of_speech, 
                                           examples, 
                                           synonyms, 
                                           antonyms, **kwargs))

    #return unique/deduped list[part_of_speech])
    def get_part_of_speech(self) -> list[str]:
        pos_list = []
        for item in self.definitions:
            pos_list.append(item.part_of_speech)
        return list(set(pos_list))

    #given part_of_speech, return definitions
    def get_definitions_part_of_speech(self, part_of_speech: str) -> list[Definition]:
        ret_list: list[Definition] = []
        for item in self.definitions:
            if item.part_of_speech == part_of_speech:
                ret_list.append(item)
        return ret_list


    def display(self) -> str:
        lines = [f"Word       : {self.word}"]

        for d in self.definitions:
            lines.append(d.part_of_speech  + " - " + d.definition)
        return "\n".join(lines)

"""         
        if self.phonetic:
            lines.append(f"Phonetic   : {self.phonetic}")

        lines.append(f"Definition : {self.definition}")

        if self.example:
            lines.append(f"Example    : {self.example}")

        if self.synonyms:
            lines.append(f"Synonyms   : {', '.join(self.synonyms)}")
 
        if self.source:
            lines.append(f"Source     : {self.source}")
"""            
        #return "\n".join(lines)
