import subprocess
import re
from utils import print_error, print_info

VERSION_FILE = "version.txt"
REGEX_VERSION_PATTERN = r"\+(\d+\.\d+\.\d+)"

'''
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
MAIN SCRIPT
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
'''

def check_version_update() -> bool:
    current_version = read_version_number()
    staged_files = get_files_to_be_committed()

    if not is_version_updated(current_version):
        print_error("Version was not updated appropriately: Current Version = {}.".format(current_version))
        return False

    if staged_files and VERSION_FILE not in staged_files:
        print_error("Version number was updated, but {} was not committed.".format(VERSION_FILE))
        return False
    
    print_info("Version number verified.")
    return True

'''
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
VERSION CLASS
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
'''

class Version:
    def __init__(self, version_string):
        '''
        Separates provided input string into major, minor, patch fields.
        Ex:
         input  => "1.2.3"
         output => major=1, minor=2, patch=3
        '''
        self.major, self.minor, self.patch = self.__convert_version_string_to_int_fields(version_string)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        if (self.major == other.major) and (self.minor == other.minor) and (self.patch == other.patch):
            return True
        return False

    def __check_version_format(self, version_string):
        '''
        Verify that the input version string matches the following format
        where each field is an integer: MAJOR.MINOR.PATCH
        '''
        version_array = version_string.split('.')

        if len(version_array) != 3:
            # Expecting 3 values which map to major, minor, and patch revisions.
            # Ex: "1.2.3"
            print_error("Version number is not long enough. Expecting versions following format: 'MAJOR.MINOR.PATCH'")
            return False

        for num in version_array:
            if not str.isnumeric(num):
                # Expecting only numeral values. No characters.
                # Ex: 1.B.3 is not allowed
                print_error("Version num is not an integer: {}".format(num))
                return False
            if int(num) < 0:
                # Negative version numbers not allowed.
                # Ex: -1.-2.-3
                print_error("Version num less than 0: {}".format(int(num)))
                return False
        return True
    
    def __convert_version_string_to_int_fields(self, version_string):
        '''
        Convert input version string to individual integer fields in the class.
        Ex: "1.2.3" results in major=1, minor=2, patch=3
        '''
        if not self.__check_version_format(version_string):
            return -1, -1, -1
        else:
            major, minor, patch = version_string.split('.')
            return int(major), int(minor), int(patch)

'''
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
HELPER FUNCTIONS
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
'''

def read_version_number() -> str:
    '''
    Read the version number from the VERSION_FILE.
    '''
    with open(VERSION_FILE, "r") as file:
        return file.read().strip()

def get_files_to_be_committed() -> list:
    try:
        output = subprocess.check_output(["git", "diff", "--staged", "--name-only"], universal_newlines=True)
        return output.strip().split("\n")
    except subprocess.CalledProcessError:
        print_error("Could not find staged files.")
        return []

def is_version_updated(current_version) -> bool:

    # # Determine if the version number has been *changed* by checking if there is a git diff in the version file.
    # git_diff = subprocess.check_output(["git", "diff", VERSION_FILE], universal_newlines=True).strip()
    # if len(git_diff) == 0:
    #     return False
    
    # Read the previous commit's version number from the 2nd line
    previous_version_char_array = subprocess.check_output(["git", "show", "HEAD", VERSION_FILE], universal_newlines=True).strip()
    version_pattern_match = re.search(REGEX_VERSION_PATTERN, previous_version_char_array)
    if version_pattern_match:
        previous_version = version_pattern_match.group(1)
    else:
        print_error("Regex could not parse previous version number.")

    # Check that the major, minor, patch numbers have been updated appropriately.
    # A: If major increases, minor and patch should == 0.
    # B: If minor increases, major should be the same as before and patch should == 0.
    # C: If patch increases, minor and major should be the same as previous.
    current_version_obj = Version(current_version)
    previous_version_obj = Version(previous_version)

    if current_version_obj.major > previous_version_obj.major: # A
        return ((current_version_obj.minor == 0) and (current_version_obj.patch == 0))
    
    elif current_version_obj.minor > previous_version_obj.minor: # B
        return ((current_version_obj.major == previous_version_obj.major) and (current_version_obj.patch == 0))
    
    elif current_version_obj.patch > previous_version_obj.patch: # C
        return ((current_version_obj.major == previous_version_obj.major) and (current_version_obj.minor == previous_version_obj.minor))
    
    elif current_version_obj == previous_version_obj:
        print_error("Current version equals the previous version at HEAD.")
        return False
    
    print_error("Version checker is returning false at default case.")
    return False

if __name__ == "__main__":
    check_version_update()
