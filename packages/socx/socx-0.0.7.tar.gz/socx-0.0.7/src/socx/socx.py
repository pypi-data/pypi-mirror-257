#!/usr/bin/env python3
try:
    import argparse
    import os
    import re
    import socket
    import hashlib
    import requests

    try:
        from . import util
    except:
        import util
except ImportError as e:
    print(
        f"""You are missing a required module ({e.name})
Try installing it with:
    pip install {e.name}
or
    python -m pip install {e.name} --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org"""
    )
    exit(1)

program_name = "socx"
VERSION = 1.0
about = f"""
Version: {VERSION}
A tool to assist with day to day activites in a security operations center (pronounced "socks")
"""

usage = f"""Usage:
    {program_name} [universal options] [function] [options]
    python {program_name}.py [universal options] [function] [options]
    
Examples:
    {program_name} info -ip 1.2.3.4
    {program_name} -v 3 info -d google.com
    {program_name} search -f filename.txt -i
    {program_name} search -f fold.*name -r
    {program_name} tools --unwrap "https://urldefense.com/v3/__https:/..."
    
"""

# TODO:
# - Add a 'alert me when IP/domain pingable changes'
# - Add CSV search
# - Add R7/S1 Asset Search
# - Add Key Encryption/Decryption


def unwrap_url(url):
    pp_decoder = util.URLDefenseDecoder()
    url = pp_decoder.decode(url)
    if "safelinks" in url:
        url = url.split("url=")[1]
    url = pp_decoder.decode(url)
    return url


def main():
    parser = argparse.ArgumentParser(prog=program_name, description=about, usage=usage)
    subparsers = parser.add_subparsers(dest="function", help="Function to perform")

    # Universal Arguments
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=1,
        help="The verbosity, 0 for quiet, 5 for very verbose",
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="Edit the settings, keys, and variables",
    )

    # Information - Online
    info = subparsers.add_parser(
        "info", help="Gather information on the specified topic"
    )
    info.add_argument("-ip", "--ip", type=str, help="An IP address")
    info.add_argument("-d", "--domain", type=str, help="A domain (google.com)")
    # add URL, Hash?

    # Search - Local
    search = subparsers.add_parser(
        "search", help="Search this machine for the specified topic"
    )
    search.add_argument("-f", "--filename", type=str, help="A file or folder name")
    search.add_argument(
        "-r", "--regex", action="store_true", help="The query is a regex pattern"
    )
    search.add_argument(
        "-a",
        "--find_all",
        action="store_true",
        help="Find all occurances (default is find first)",
    )
    search.add_argument(
        "-i",
        "--insensitive",
        action="store_true",
        help="Search case insensitive (default is case sensitive)",
    )
    # Filename, Hash, registrykey?

    # Tools - Local
    tools = subparsers.add_parser("tools", help="Use tools to perform a function")
    tools.add_argument(
        "-u",
        "--unwrap",
        type=str,
        help="A URL to unwrap (remove safelinks and protectlinks)",
    )

    args = parser.parse_args()

    ##########
    ## Util ##
    ##########

    def p(*args_, v=1, end="\n", sep=" ", file=None):
        if args.verbosity >= v:
            print(*args_, end=end, sep=sep, file=file)

    ############
    ## Config ##
    ############

    environmental_variables = {"InsightVMAPI_BASE_URL": "", "InsightVMAPI_KEY": ""}

    def get_enironmental_variable(name):
        value = os.environ.get("_socX__" + name)
        if value is None:
            value = environmental_variables[name]
        return value

    if args.config:
        while True:
            p("Settings, keys, variables", v=1)
            for index, var in enumerate(environmental_variables.keys()):
                print(f"\t{index} - {var}")
            index = input(
                "Enter the index of the variable you want to edit (Nothing to stop): "
            )
            if index == "":
                break
            else:
                index = int(index)
            p(f"Editing '{list(environmental_variables.keys())[index]}'", v=1)
            old_value = get_enironmental_variable(
                list(environmental_variables.keys())[index]
            )
            print(f"Old value:'{old_value}'")
            new_value = input("New value (Nothing to cancel): ")
            if new_value == "":
                continue
            os.environ["_socX__" + list(environmental_variables.keys())[index]] = (
                new_value
            )
            p("Value updated\n", v=1)

    ##########
    ## Info ##
    ##########

    def print_ip_info(ip):
        try:
            response = requests.request("GET", url=f"https://ipinfo.io/{args.ip}/json")
            ip_service = "ipinfo"
        except:
            p("Failed to get information from ipinfo.io", v=3)
            response = requests.request("GET", url=f"http://ipwho.is/{args.ip}")
            ip_service = "ipwhois"
        for key, item in response.json().items():
            if args.verbosity > 0:
                print(f"({ip_service}) {key}: {item}")
            else:
                print(f"{key}: {item}")

    if args.function == "info":
        if args.ip:
            p(f"Getting information on {args.ip}", v=1)
            try:
                hostname = socket.gethostbyaddr(args.ip)
                print(f"Hostname: {hostname}")
            except Exception as e:
                p(f"Hostname: Error - {e}", v=1)
            # WINDOWS SPECIFIC
            ping_response = os.system(f"ping -n 1 {args.ip} > nul")
            if ping_response == 0:
                print(f"Ping: {args.ip} is up")
            else:
                print(f"Ping: {args.ip} is down")
            print_ip_info(args.ip)
            # Rapid7
            if (
                get_enironmental_variable("InsightVMAPI_BASE_URL") != ""
                and get_enironmental_variable("InsightVMAPI_KEY") != ""
            ):
                ivm = util.InsightVM(
                    get_enironmental_variable("InsightVMAPI_BASE_URL"),
                    get_enironmental_variable("InsightVMAPI_KEY"),
                )
                for asset in ivm.ip_search(args.ip):
                    print(ivm._format_return_string(asset))
        elif args.domain:
            if args.domain.startswith("http"):
                args.domain = args.domain.split("//")[1]
            if args.domain.startswith("www."):
                args.domain = args.domain.split("www.")[1]
            p(f"Getting information on {args.domain}", v=1)
            try:
                ip = socket.gethostbyname(args.domain)
                print(f"IP: {ip}")
            except Exception as e:
                p(f"IP: Error - {e}", v=1)
            # WINDOWS SPECIFIC
            ping_response = os.system(f"ping -n 1 {args.domain} > nul")
            if ping_response == 0:
                print(f"Ping: {args.domain} is up")
            else:
                print(f"Ping: {args.domain} is down")

            print_ip_info(ip)
            print(f"Whois record: https://www.whois.com/whois/{args.domain}")

    ############
    ## Search ##
    ############

    def search(pattern, string):
        if args.insensitive:
            return re.search(pattern, string, re.IGNORECASE)
        else:
            return re.search(pattern, string)

    def find_file(filename, directory=os.getcwd(), find_all=False):
        files_found = []
        filename_copy = filename
        if args.insensitive and not args.regex:
            filename = filename.lower()
        for root, dirs, files in os.walk(directory):
            if args.regex:
                r_files = [
                    os.path.join(root, file)
                    for file in files + dirs
                    if search(filename, file)
                ]
                if find_all:
                    files_found.extend(r_files)
                elif len(r_files) > 0:
                    return r_files[0]
            else:
                if args.insensitive:
                    files = [file.lower() for file in files]
                    dirs = [dir.lower() for dir in dirs]
                if filename in files or filename in dirs:
                    if find_all:
                        files_found.append(os.path.join(root, filename_copy))
                    else:
                        return os.path.join(root, filename_copy)

        if find_all:
            return files_found
        else:
            return None

    if args.function == "search":
        if args.filename:
            p(f"Searching for {args.filename}", v=1)
            if args.insensitive:
                p("Performing case insensitive search", v=3)
            if args.find_all:
                p("Finding all occurances", v=3)
            # WINDOWS SPECIFIC
            if args.find_all:
                result = find_file(args.filename, "C:\\", True)
                result = result + find_file(args.filename, "D:\\", True)
                result = set(result)
                if len(result) == 0:
                    print("File/Folder not found")
                else:
                    for file in result:
                        print(f"File/Folder found at {file}")
            else:
                result = find_file(args.filename, os.path.dirname(os.getcwd()))
                if result is None:
                    result = find_file(args.filename, os.path.expanduser("~"))
                if result is None:
                    result = find_file(args.filename, "C:\\")
                if result is None:
                    result = find_file(args.filename, "D:\\")
                if result is None:
                    print("File/Folder not found")
                else:
                    print(f"File/Folder found at {result}")

        elif args.hash:
            p(f"Searching for {args.hash}", v=1)
            # WINDOWS SPECIFIC

            def calculate_hash(file_path, algorithm="sha256"):
                """Calculate the hash of a file."""
                hash_func = getattr(hashlib, algorithm.lower(), None)
                if hash_func is None:
                    raise ValueError(f"Invalid hash algorithm: {algorithm}")

                # Read the file in binary mode and compute the hash
                with open(file_path, "rb") as f:
                    hash_obj = hash_func()
                    while chunk := f.read(4096):  # Read in chunks to handle large files
                        hash_obj.update(chunk)

                return hash_obj.hexdigest()

            def search_hash(file_path, target_hash, algorithm="sha256"):
                """Search for a specific hash in a file."""
                file_hash = calculate_hash(file_path, algorithm)
                return file_hash == target_hash

            # Example usage:
            file_path = "path/to/your/file"
            target_hash = "put your target hash here"
            algorithm = "sha256"  # Specify the hashing algorithm if needed

            if search_hash(file_path, target_hash, algorithm):
                print("Hash found in the file.")
            else:
                print("Hash not found in the file.")

    ###########
    ## Tools ##
    ###########
    if args.function == "tools":
        # Test Link: https://urldefense.com/v3/__https:/conferences.stjude.org/g87vv8?i=2NejfAgCkki403xbcRpHuw&locale=en-US__;!!NfcMrC8AwgI!cq3afLDXviFyix2KeJ62VsQBrrZOgfyZu1fks7uQorRGX6VOgcDaUgTpxFdJRmXMdtU5zsmZB9PUw-TmquYgbIGIYUDPsQ$
        # Test Link:
        if args.unwrap:
            p("Unwrapping URL\n", v=3)
            print(f"Unwrapped URL:\n{unwrap_url(args.unwrap)}")
            p("\n", v=3)


if __name__ == "__main__":
    main()
