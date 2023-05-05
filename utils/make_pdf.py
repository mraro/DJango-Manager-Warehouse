import fpdf
from datetime import datetime


class PDF(fpdf.FPDF):
    def __init__(self, receiver,  len_table, title_table, *args, orientation='P', unit='mm', format='A4'):
        """ Give me a name a user, size_table, tr_table """
        super().__init__(orientation, unit, format)
        self.receive = receiver
        self.list_values = args
        self.cell_widths = len_table

        self.tr = [self.cell_widths, title_table]

    def my_title(self):
        # Add Title
        self.set_font('Arial', 'B', 19)
        self.cell(w=0, h=30, txt="Documento de Saida", border=0, ln=1, align='C')

    def basic_table(self, content):
        # Set First line where is title table
        for x in range(len(self.tr[0])):
            # print(self.tr[0][x])
            self.cell(self.tr[0][x], 7, self.tr[1][x], 1)
        self.ln()

        # Add data on table
        for row in content:
            for x in range(len(row)):
                self.cell(self.cell_widths[x], 7, str(row[x]), 1)
            self.ln()

    def chapter_body(self, content, title):
        # Add Title before the table

        self.set_font('Arial', 'B', 15)
        self.multi_cell(w=0, h=10, txt=title, border=0, align='C')
        self.cell(w=0, h=10, txt="Itens", border=0, ln=1, align='L')
        # call table
        self.basic_table(content)

    def footer(self):
        # Add footer with signature field
        self.set_y(-35)
        self.set_font('Arial', '', 8)
        # Add line to signature
        self.cell(w=0, h=10, txt=f'____________________________________________________________          '
                                 f'     _____________________________________________________', border=0, ln=1,
                  align='L')  # noqa
        self.set_font('Arial', '', 12)
        # above the line
        self.cell(w=0, h=10, txt=f'                Responsável do Almoxarifado                  '
                                 f'                                    {self.receive}', border=0, ln=1,
                  align='L')  # noqa
        self.set_font('Arial', '', 9)

        self.cell(w=0, h=10, txt='Criado em ' + str(datetime.now()), border=0, ln=1, align='L')

    def print_chapter(self, content, title):
        """ give me a list[[row],[row],[row]] and a title(str)"""
        self.my_title()
        self.chapter_body(content, title)


if __name__ == "__main__":
    len_table = [20, 150, 20]
    title_table = ['INV', 'Nome do Equipamento', 'Qtd']
    data = [['id', 'nome', 'quantity'],
            ['id2', 'nome', 'quantity'],
            ['id3', 'nome', 'quantity']]
    # Create PDF:
    pdf = PDF("Fulano", len_table, title_table)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.print_chapter( data, "TESTE")
    # Save:
    pdf.output('document.pdf', 'F')
