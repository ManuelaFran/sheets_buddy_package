# SheetsBuddy
SheetsBuddy é uma biblioteca Python para automatizar interações com o Google Sheets, facilitando tarefas como leitura, escrita, formatação e exportação de dados.

## Instalação
```bash
pip install sheetsbuddy
```
## Uso Básico
```
from sheetsbuddy import SheetsBuddy

# Inicialize a classe com o caminho para o JSON das credenciais e o link da planilha
buddy = SheetsBuddy('path/to/credentials.json', 'https://docs.google.com/spreadsheets/d/your_sheet_id')

# Adicionar uma fórmula
buddy.add_formula('A1', 'SUM(B1:B10)')

# Aplicar formatação
buddy.apply_bulk_formatting('A1:C10', color={'red': 1, 'green': 0.9, 'blue': 0.9}, bold=True, font_size=12)

# Exportar para CSV
buddy.export_to_csv('Sheet1', 'dados.csv')

# Exportar para JSON
buddy.export_to_json('Sheet1', 'dados.json')
```
## Funcionalidades
- Conexão automática com planilhas via URL
- Adição de fórmulas com separadores personalizados
- Aplicação de formatações em massa
- Exportação de dados para CSV e JSON

## Licença
MIT License