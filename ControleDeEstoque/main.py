from DataBase.crud import DataBase
from PyQt5 import uic, QtWidgets


#                                       Tela Principal
def AbrirTelaPrincial():
    TelaPrincipal.show()
    TelaProduto.close()
    TelaCliente.close()
    TelaVerProduto.close()
    TelaVerCliente.close()

def AtualizarTelaPrincipal():
    totalClientes = bd.TamanhoTabela("clientes")
    TelaPrincipal.lbTotalClientes.setText(str(totalClientes))

    totalInformatica = bd.TamanhoTabela("informatica")
    TelaPrincipal.lbTotaInformatica.setText(str(totalInformatica))

    totalBebidas = bd.TamanhoTabela("Bebidas")
    TelaPrincipal.lbTotaIBebidas.setText(str(totalBebidas))

    totalCongelados = bd.TamanhoTabela("Congelados")
    TelaPrincipal.lbTotaICongelados.setText(str(totalCongelados))

    totalUtilidades = bd.TamanhoTabela("Utilidades")
    TelaPrincipal.lbTotaIUtilidades.setText(str(totalUtilidades))

    totalFrutas = bd.TamanhoTabela("Frutas")
    TelaPrincipal.lbTotaIFrutas.setText(str(totalFrutas))

#                                       Produtos

def Produtos():
    TelaPrincipal.close()
    TelaProduto.show()   

def CadastrarPruduto():
    try:
        categoria = TelaProduto.cbCategoria.currentText()
        codigo = TelaProduto.inputCodigo.text()
        nome = TelaProduto.inputNome.text()
        quantidade = TelaProduto.inputQuantidade.text()
        preco = TelaProduto.inputPreco.text().replace(',', '.')
        descricao = TelaProduto.inputDescricao.text()
        bd.CreateTB(categoria)

        if (codigo and nome and quantidade and preco and descricao) != '':
            bd.InsertValues(categoria,codigo, nome, quantidade, preco, descricao)
            TelaProduto.lbResposta.setText('Dados Cadastrado com sucesso!')
            print('Dados Cadastrado com sucesso!')
        else:
            print('Prencha todos os campos acima')
            TelaProduto.lbResposta.setText('Prencha todos os campos acima')
    except Exception as error:
        print('Error', error)

    TelaProduto.inputCodigo.setText('')
    TelaProduto.inputNome.setText('')
    TelaProduto.inputQuantidade.setText('')
    TelaProduto.inputPreco.setText('')
    TelaProduto.inputDescricao.setText('')
    AtualizarTelaPrincipal()

def VerProdutos():
    TelaVerProduto.show()

    AtulizarDados()

    categoria = TelaVerProduto.cbCategoria.currentText()
    bd.CreateTB(categoria)

    dados_lidos = DataBase.ViewData(bd,categoria)
    TelaVerProduto.tableWidget.setRowCount(len(dados_lidos))
    TelaVerProduto.tableWidget.setColumnCount(6)

    for linha in range(0, len(dados_lidos)):
            for coluna in range(0, 6):
                TelaVerProduto.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

def AtulizarDados():
    TelaVerProduto.tableWidget.clearContents()
    categoria = TelaVerProduto.cbCategoria.currentText()
    dados_lidos = DataBase.ViewData(bd,categoria)
    TelaVerProduto.tableWidget.setRowCount(len(dados_lidos))
    TelaVerProduto.tableWidget.setColumnCount(6)
    for linha in range(0, len(dados_lidos)):
            for coluna in range(0, 6):
                TelaVerProduto.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

def PesquisarProdutos():
    pesquisa = TelaVerProduto.inputPesquisa.text()
    categoria = TelaVerProduto.cbCategoria.currentText()
    dados_lidos = DataBase.SearchValues(bd,categoria,"name",pesquisa)

    TelaVerProduto.tableWidget.setRowCount(len(dados_lidos))
    TelaVerProduto.tableWidget.setColumnCount(6)

    for linha in range(0, len(dados_lidos)):
            for coluna in range(0, 6):
                TelaVerProduto.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

def ExcluirProduto():
    categoria = TelaVerProduto.cbCategoria.currentText()
    
    linha = TelaVerProduto.tableWidget.currentRow()
    TelaVerProduto.tableWidget.removeRow(linha)  
    bd.cursor.execute(f"SELECT id FROM {categoria};")
    dados_lidos = bd.cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    bd.cursor.execute(f"DELETE FROM {categoria} WHERE id="+ str(valor_id))
    bd.cursor.commit()

def EditarProduto():
    TelaVerProduto.close()
    global numero_id
    categoria = TelaVerProduto.cbCategoria.currentText()

    linha = TelaVerProduto.tableWidget.currentRow()
    
    bd.cursor.execute(f"SELECT id FROM {categoria};")
    dados_lidos = bd.cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    bd.cursor.execute(f"SELECT * FROM {categoria} WHERE id="+ str(valor_id))
    produto = bd.cursor.fetchall()
    TelaEditarProduto.inputID.setText(str(produto[0][0]))
    TelaEditarProduto.inputCodigo.setText(str(produto[0][1]))
    TelaEditarProduto.inputNome.setText(str(produto[0][2]))
    TelaEditarProduto.inputQuantidade.setText(str(produto[0][3]))
    TelaEditarProduto.inputPreco.setText(str(produto[0][4]))
    TelaEditarProduto.inputDescricao.setText(str(produto[0][5]))
    numero_id = valor_id
    TelaEditarProduto.show()

def SalvarProduto():
    global numero_id
    categoria = TelaVerProduto.cbCategoria.currentText()

    codigo = TelaEditarProduto.inputCodigo.text()
    nome = TelaEditarProduto.inputNome.text()
    quantidade = TelaEditarProduto.inputQuantidade.text()
    preco = TelaEditarProduto.inputPreco.text()
    descricao = TelaEditarProduto.inputDescricao.text()

    bd.cursor.execute(f"UPDATE {categoria} SET code = '{codigo}', name = '{nome}', amount = '{quantidade}', price = '{preco}', description ='{descricao}' WHERE id = {numero_id}")
    bd.cursor.commit()

    TelaEditarProduto.close()
    AtulizarDados()
    TelaVerProduto.show()

#                                       Clientes

def Clientes():
    TelaPrincipal.close()
    TelaCliente.show()

def CadastrarCliente():
    try:
        nome = TelaCliente.inputNome.text()
        cpf = TelaCliente.inputCPF.text()
        rg = TelaCliente.inputRG.text()
        celular = TelaCliente.inputCelular.text()
        email = TelaCliente.inputEmail.text()
        bd.CreateTBClientes()

        if (nome and cpf and rg and celular and email) != '':
            bd.InsertCliente('clientes',nome, cpf, rg, celular, email)
            TelaCliente.lbResposta.setText('Dados Cadastrado com sucesso!')
            print('Dados Cadastrado com sucesso!')
        else:
            print('Prencha todos os campos acima')
            TelaCliente.lbResposta.setText('Prencha todos os campos acima')
    except Exception as error:
        print('Error', error)

    TelaCliente.inputNome.setText('')
    TelaCliente.inputCPF.setText('')
    TelaCliente.inputRG.setText('')
    TelaCliente.inputCelular.setText('')
    TelaCliente.inputEmail.setText('')
    AtualizarTelaPrincipal()

def VerClientes():
    TelaVerCliente.show()

    categoria = TelaVerCliente.cbCategoria.currentText()
    bd.CreateTB(categoria)

    dados_lidos = DataBase.ViewData(bd,categoria)
    TelaVerCliente.tableWidget.setRowCount(len(dados_lidos))
    TelaVerCliente.tableWidget.setColumnCount(6)

    for linha in range(0, len(dados_lidos)):
            for coluna in range(0, 6):
                TelaVerCliente.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

def ExcluirCliente():
    categoria = TelaVerCliente.cbCategoria.currentText()
    
    linha = TelaVerCliente.tableWidget.currentRow()
    TelaVerCliente.tableWidget.removeRow(linha)  
    bd.cursor.execute(f"SELECT id FROM {categoria};")
    dados_lidos = bd.cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    bd.cursor.execute(f"DELETE FROM {categoria} WHERE id="+ str(valor_id))
    bd.cursor.commit()

def EditarCliente():
    TelaVerCliente.close()
    global numero_id
    categoria = TelaVerCliente.cbCategoria.currentText()

    linha = TelaVerCliente.tableWidget.currentRow()
    
    bd.cursor.execute(f"SELECT id FROM {categoria};")
    dados_lidos = bd.cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    bd.cursor.execute(f"SELECT * FROM {categoria} WHERE id="+ str(valor_id))
    cliente = bd.cursor.fetchall()
    TelaEditarCliente.inputID.setText(str(cliente[0][0]))
    TelaEditarCliente.inputNome.setText(str(cliente[0][1]))
    TelaEditarCliente.inputCPF.setText(str(cliente[0][2]))
    TelaEditarCliente.inputRG.setText(str(cliente[0][3]))
    TelaEditarCliente.inputCelular.setText(str(cliente[0][4]))
    TelaEditarCliente.inputEmail.setText(str(cliente[0][5]))
    numero_id = valor_id
    TelaEditarCliente.show()

def AtulizarClientes():
    TelaVerCliente.tableWidget.clearContents()
    categoria = TelaVerCliente.cbCategoria.currentText()
    dados_lidos = DataBase.ViewData(bd,categoria)
    TelaVerCliente.tableWidget.setRowCount(len(dados_lidos))
    TelaVerCliente.tableWidget.setColumnCount(6)
    for linha in range(0, len(dados_lidos)):
            for coluna in range(0, 6):
                TelaVerCliente.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))

def SalvarCliente():
    global numero_id
    categoria = TelaVerCliente.cbCategoria.currentText()

    nome = TelaEditarCliente.inputNome.text()
    cpf = TelaEditarCliente.inputCPF.text()
    rg = TelaEditarCliente.inputRG.text()
    celular = TelaEditarCliente.inputCelular.text()
    email = TelaEditarCliente.inputEmail.text()

    bd.cursor.execute(f"UPDATE {categoria} SET nome = '{nome}', cpf = '{cpf}', rg = '{rg}', celular = '{celular}', email ='{email}' WHERE id = {numero_id}")
    bd.cursor.commit()

    TelaEditarCliente.close()
    AtulizarClientes()
    TelaVerCliente.show()

def PesquisarClientes():
    pesquisa = TelaVerCliente.inputPesquisa.text()
    categoria = TelaVerCliente.cbCategoria.currentText()
    dados_lidos = DataBase.SearchValues(bd,categoria,"nome",pesquisa)

    TelaVerCliente.tableWidget.setRowCount(len(dados_lidos))
    TelaVerCliente.tableWidget.setColumnCount(6)

    for linha in range(0, len(dados_lidos)):
            for coluna in range(0, 6):
                TelaVerCliente.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))
                

bd = DataBase('Estoque')

app = QtWidgets.QApplication([])

# Tela Inicial
TelaPrincipal = uic.loadUi('interface/TelaPrincipal.ui')
TelaPrincipal.actionCadastrarProduto.triggered.connect(Produtos)
TelaPrincipal.actionVerProdutos.triggered.connect(VerProdutos)
TelaPrincipal.actionVerClientes.triggered.connect(VerClientes)
TelaPrincipal.actionCadastrarCliente.triggered.connect(Clientes)
AtualizarTelaPrincipal()

# Tela Produto
TelaProduto = uic.loadUi('interface/Produtos.ui')
TelaProduto.btnCadastrar.clicked.connect(CadastrarPruduto)
TelaProduto.actionTelaPrincipal.triggered.connect(AbrirTelaPrincial)

# Tela Ver Produtos
TelaVerProduto = uic.loadUi('interface/VerProdutos.ui')
TelaVerProduto.btnAtualizar.clicked.connect(AtulizarDados)
TelaVerProduto.btnPesquisar.clicked.connect(PesquisarProdutos)
TelaVerProduto.btnExcluir.clicked.connect(ExcluirProduto)
TelaVerProduto.btnEditar.clicked.connect(EditarProduto)
TelaVerProduto.actionTelaPrincipal.triggered.connect(AbrirTelaPrincial)

# Tela Editar Produtos
TelaEditarProduto = uic.loadUi('interface/EditarProdutos.ui')
TelaEditarProduto.btnSalvar.clicked.connect(SalvarProduto)

# Tela Cliente
TelaCliente = uic.loadUi('interface/Clientes.ui')
TelaCliente.btnCadastrar.clicked.connect(CadastrarCliente)
TelaCliente.actionTelaPrincipal.triggered.connect(AbrirTelaPrincial)

# Tela Ver Cliente
TelaVerCliente = uic.loadUi('interface/VerClientes.ui')
TelaVerCliente.actionTelaPrincipal.triggered.connect(AbrirTelaPrincial)
TelaVerCliente.btnExcluir.clicked.connect(ExcluirCliente)
TelaVerCliente.btnEditar.clicked.connect(EditarCliente)
TelaVerCliente.btnPesquisar.clicked.connect(PesquisarClientes)

# Tela Editar Cliente
TelaEditarCliente= uic.loadUi('interface/EditarClientes.ui')
TelaEditarCliente.btnSalvar.clicked.connect(SalvarCliente)

TelaPrincipal.show()
app.exec()
