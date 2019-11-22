import os
import argparse
import subprocess


OUTPUT_DIRECTORY = "NETWORK_SCANS"
RAW_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY + "/RAW_MASSCANS"
PRETTY_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY + "/PRETTY_SCANS"
NMAP_OUTPUT_DIRECTORY = OUTPUT_DIRECTORY + "/NMAP_SCANS"


def handle_arguments():
    """
    Initialize the arguments for the script.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--skipscan",
        help="Skip the masscan scan, presume target_subnet is a file.",
        action="store_true",
    )
    parser.add_argument(
        "target_subnet",
        help="The subnet to scan, or if -s is specified, path to a raw masscan scan.",
    )
    parser.add_argument(
        "-p",
        "--ports",
        help="Specify the ports to scan, 0-65535 by default.",
        default="0-65535",
    )
    parser.add_argument(
        "-f", "--format", help="Prettify the raw masscan output.", action="store_true"
    )
    parser.add_argument(
        "-n",
        "--nmap",
        help="Refer results to an aggressive nmap service scan.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--vuln",
        help="Scan using nmap's vuln script. Requires the nmap argument.",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--ignoreports",
        help="Comma separated list of ports to ignore for the vuln script scan.",
        action="store_true",
    )
    return parser.parse_args()


def read_file_to_string(filepath):
    """
    Read a file into a string.
    :param filepath: File to read.
    :return: File content as a string.
    """
    with open(filepath, "r") as file:
        file_content = file.read()
    return file_content


def parse_raw_masscan_output(raw_output):
    """
    Parses raw masscan output into a dictionary of IPs to a list of ports.
    :param raw_output: The raw output of a masscan scan.
    :return: Dictionary of IPs to a list of ports.
    """
    output_lines = raw_output.split("\n")

    ip_ports = {}
    # Extract ports for IPs.
    for line in output_lines:
        split_line = line.strip().split(" ")
        if (
            len(split_line) != 5
        ):  # Lines with ports have 4 spaces, so 5 elements if we split by space.
            continue

        ip = split_line[3]
        port = split_line[2]

        if ip in ip_ports.keys():
            ip_ports[ip].append(port)
        else:
            ip_ports[ip] = []
            ip_ports[ip].append(port)
    return ip_ports


def main():
    """
    Scan a subnet using masscan and optionally prettify the output.
    :return: None
    """
    args = handle_arguments()

    target_subnet = args.target_subnet

    if not args.skipscan:
        slashless_target_subnet = target_subnet.replace("/", "-")

        masscan_list_file = os.path.join(
            RAW_OUTPUT_DIRECTORY, "raw_masscan_list_" + slashless_target_subnet + ".txt"
        )
        masscan_command = [
            "masscan",
            target_subnet,
            "-p" + args.ports,
            "--rate",
            "100000",
            "-oL",
            masscan_list_file,
        ]

        print("== INITIATING MASSCAN ON SUBNET %s" % target_subnet)

        # Ensure that the output directory exists, create it if it doesn't.
        if not os.path.exists(OUTPUT_DIRECTORY) or not os.path.exists(
            RAW_OUTPUT_DIRECTORY
        ):
            os.makedirs(RAW_OUTPUT_DIRECTORY)

        subprocess.Popen(masscan_command).wait()

        print("== MASSCAN COMPLETED ON SUBNET %s" % target_subnet)

        if not os.path.exists(masscan_list_file):
            raise Exception("ERROR, masscan raw output does not exist.")
    else:
        masscan_list_file = target_subnet
        if not os.path.exists(masscan_list_file):
            raise Exception("ERROR, masscan raw output does not exist.")

        split_masscan_filename = os.path.basename(masscan_list_file).split(
            "_"
        )  # Split the raw filename to get the target subnet
        target_subnet = str(split_masscan_filename[len(split_masscan_filename) - 1])
        slashless_target_subnet = target_subnet.replace("/", "-")

    # A map of IPs and their respective ports. Used by the prettifier and aggressive NMAP scanner.
    ip_ports = None
    if args.format:
        # Ensure that the pretty output directory exists, create it if it doesn't.
        if not os.path.exists(PRETTY_OUTPUT_DIRECTORY):
            os.makedirs(PRETTY_OUTPUT_DIRECTORY)

        masscan_pretty_file = os.path.join(
            PRETTY_OUTPUT_DIRECTORY,
            "pretty_masscan_" + slashless_target_subnet + ".txt",
        )
        print("== PRETTIFYING RAW OUTPUT to %s" % masscan_pretty_file)

        raw_masscan_output = read_file_to_string(masscan_list_file)
        with open(masscan_pretty_file, "w") as pretty_file:
            ip_ports = parse_raw_masscan_output(raw_masscan_output)

            # Write to prettified output.
            for ip in sorted(ip_ports.keys()):
                sorted_ports = sorted(ip_ports[ip])
                output_string = "%s: %s\n" % (ip, ", ".join(sorted_ports))
                pretty_file.write(output_string)

        print("== PRETTIFIED RAW OUTPUT to %s" % masscan_pretty_file)

    if args.nmap:
        # Ensure that the pretty output directory exists, create it if it doesn't.
        if not os.path.exists(NMAP_OUTPUT_DIRECTORY):
            os.makedirs(NMAP_OUTPUT_DIRECTORY)

        # If the prettifier wasn't ran, let's generate the ip/port dictionary here.
        if not ip_ports:
            raw_masscan_output = read_file_to_string(masscan_list_file)
            ip_ports = parse_raw_masscan_output(raw_masscan_output)

        nmap_output_file = os.path.join(
            NMAP_OUTPUT_DIRECTORY, "nmap_output_" + slashless_target_subnet + ".txt"
        )

        print(
            "== STARTING NMAP SERVICE SCAN ON SUBNET %s, OUTPUT AT %s"
            % (target_subnet, nmap_output_file)
        )
        # Iterate each IP and its ports to scan.
        for ip in ip_ports.keys():
            if args.ignoreports:
                ignore_ports = args.ignoreports.split(',')
                for ignore_port in ignore_ports:
                    ip_ports[ip].remove(ignore_port)
            ports_string = ",".join(ip_ports[ip])  # Used in nmap's port argumment

            # Aggressive scan without DOSing the network.
            nmap_command = [
                "nmap",
                "-T5",
                "-sV",
                "-sT",
                "-p" + ports_string,
                "--append-output",
                "-oN",
                nmap_output_file,
                "--min-rate=100000",
                "-Pn",
                ip,
            ]
            if args.vuln:
                nmap_command.extend(["--script", "vuln"])

            print(
                "== STARTING NMAP SERVICE SCAN ON IP %s PORTS %s"
                % (ip, ",".join(ip_ports[ip]))
            )
            subprocess.Popen(nmap_command).wait()
            print("== FINISHED NMAP SERVICE SCAN ON IP %s" % ip)

        print(
            "== FINISHED NMAP SERVICE SCAN ON SUBNET %s, OUTPUT AT %s"
            % (target_subnet, nmap_output_file)
        )


if __name__ == "__main__":
    main()
