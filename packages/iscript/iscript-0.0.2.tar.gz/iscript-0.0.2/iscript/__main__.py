from sys import argv
import os
from rich import print as rprint
from json import loads

from iscript.FrontEnd.Lexer import Lexer
from iscript.FrontEnd.Parser import Parser
from iscript.BackEnd.Core import Core
from iscript.FrontEnd.funcsForCommands import *


def newProject(name: str):
    pathToProject: str = os.getcwd()

    # Создание папки с проектом
    if os.path.exists(name):
        rprint('[red]<IS> There is already a project with the same name!')
        exit(1)
    else:
        os.mkdir(name)

    # Инициализация главного файла
    with open( os.path.join(pathToProject, name, 'main.is'), 'w', encoding='utf-8' ) as file:
        file.write((
            '-- New project!\n'
            'WHEN MESSAGE IS "/start" {\n'
            '   SEND TEXT "Hello user!"\n'
            '}\n'
        ))

    # Инициализация главного файла
    with open( os.path.join(pathToProject, name, 'conf.json'), 'w', encoding='utf-8' ) as file:
        file.write((
            '{\n'
            '   "token": null\n'
            '}\n'
        ))

    # Создание папки с данными   
    os.mkdir( os.path.join(pathToProject, name, 'data') )
    with open( os.path.join(pathToProject, name, 'data', 'logs.json'), 'w' ):
        pass
    
    rprint('[green]<IS> The project has been successfully created!')


def runProject():
    pathToProject: str = os.getcwd()


    #########################
    # ДЛЯ ТЕСТОВ            #
    #########################
    os.chdir('C:/Users/1/Desktop/Immeptor/immeptorScript/Interpretator/Test/')
    pathToProject = 'C:/Users/1/Desktop/Immeptor/immeptorScript/Interpretator/Test/'
    #########################

    # Открытие файла с кодом
    with open( os.path.join( pathToProject + '/main.is' ), 'r', encoding='utf-8') as file:
        code: str = file.read()

    # Открытие файла с настройками
    with open( os.path.join( pathToProject + '/conf.json' ), 'r', encoding='utf-8') as file:
        settings: dict = loads( file.read() )


    lex = Lexer()
    # lex.show( code )

    tokens = lex.build(code)
    

    pars = Parser()
    programm = pars.getAST(tokens)

    CV: Core = Core(settings, programm)
    CV.run()



if __name__ == '__main__':
    match argv[1:]:
        case ['new', name]:
            newProject(name)

        case ['run']:
            runProject()

        case ['info']:
            rprint(
                '[violet]<IS> Information about the current version of ImmeptorScript[/]\n'
                '[blue]*[/] Current version: [green]0.0.1[/]\n'
                '[blue]*[/] Author: [green]Immeptor Group[/]\n'
                '[blue]*[/] Link: [green]https://immeptor.script.ru/[/]\n'
                '[blue]*[/] PyPI: [green]https://u/[/]\n'
                '[blue]*[/] GitHub: [green]https://github.com/ITAplle/ImmeptorScript[/]'
            )

        case _:
            rprint((
                '[red]<IS> There is no such console command!\n'
                'Maybe this will help you:\n'
                '* py -m ImScript new <name> - creating a new project\n'
                '* py -m ImScript run - run a project'
            ))
            exit(1)