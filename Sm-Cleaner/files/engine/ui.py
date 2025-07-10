import os
import sys
import time
from colorama import init, Fore, Style
from engine.diagnostics import SystemDiagnostics
from engine.fixes import SystemFixes
from engine.utils import clear_screen, format_size, get_choice, print_section
from data.ascii_art import ASCII_ART
from data.ascii_art import diagnostics
from data.ascii_art import fixes, sss

init(autoreset=True)


class ConsoleInterface:
    def __init__(self):
        self.diagnostics = SystemDiagnostics()
        self.fixes = SystemFixes()
        self.WIDTH = 100
        self.COLORS = {
            'title': Fore.CYAN + Style.BRIGHT,
            'menu': Fore.YELLOW,
            'option': Fore.GREEN,
            'warning': Fore.RED,
            'success': Fore.GREEN,
            'info': Fore.BLUE
        }

    def draw_header(self, title):
        clear_screen()
        print(f"\n{self.COLORS['title']}{'═' * self.WIDTH}")
        print(f"║{title.center(self.WIDTH - 2)}║")
        print(f"{'═' * self.WIDTH}{Style.RESET_ALL}\n")

    def main_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            print(ASCII_ART)
            print("")
            print(f"[ 1 ] Диагностика системы")
            print(f"[ 2 ] Решение проблем")
            print(f"[ 3 ] Оптимизация Windows")
            print(f"[ 4 ] Мониторинг в реальном времени")
            print(f"[ 5 ] Выход")
            print("")

            choice = get_choice(1, 5)

            if choice == 1:
                self.diagnostics_menu()
            elif choice == 2:
                self.fixes_menu()
            elif choice == 3:
                self.optimization_menu()
            elif choice == 4:
                self.real_time_monitor()
            elif choice == 5:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(sss)
                time.sleep(3)
                sys.exit(0)

    def diagnostics_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(diagnostics)
            print("")
            print(f"[ 1 ] Общая информация о системе")
            print(f"[ 2 ] Статус компонентов")
            print(f"[ 3 ] Процессор")
            print(f"[ 4 ] Оперативная память")
            print(f"[ 5 ] Диски и накопители")
            print(f"[ 6 ] Сеть и интернет")
            print(f"[ 7 ] Безопасность")
            print(f"[ 8 ] Процессы и службы")
            print(f"[ 9 ] Аппаратные датчики")
            print(f"[ 10 ] Полный отчет")
            print(f"[ 0 ] Назад в главное меню")
            print("")

            choice = get_choice(0, 10)

            if choice == 0:
                return
            elif choice == 1:
                self.diagnostics.general_info()
            elif choice == 2:
                self.diagnostics.components_status()
            elif choice == 3:
                self.diagnostics.cpu_info()
            elif choice == 4:
                self.diagnostics.ram_info()
            elif choice == 5:
                self.diagnostics.disks_info()
            elif choice == 6:
                self.diagnostics.network_info()
            elif choice == 7:
                self.diagnostics.security_info()
            elif choice == 8:
                self.diagnostics.processes_info()
            elif choice == 9:
                self.diagnostics.sensors_info()
            elif choice == 10:
                self.diagnostics.full_report()

            input("\nНажмите Enter для продолжения...")

    def fixes_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(fixes)
            print("")
            print(f"[ 1 ] Закрыть опасные порты")
            print(f"[ 2 ] Оптимизировать работу процессора")
            print(f"[ 3 ] Освободить оперативную память")
            print(f"[ 4 ] Очистить диск от мусора")
            print(f"[ 5 ] Исправить сетевые проблемы")
            print(f"[ 6 ] Повысить безопасность системы")
            print(f"[ 7 ] Управление автозагрузкой")
            print(f"[ 8 ] Восстановление системных файлов")
            print(f"[ 0 ] Назад в главное меню")
            print("")

            choice = get_choice(0, 8)

            if choice == 0:
                return
            elif choice == 1:
                self.fixes.close_dangerous_ports()
            elif choice == 2:
                self.fixes.optimize_cpu()
            elif choice == 3:
                self.fixes.free_up_ram()
            elif choice == 4:
                self.fixes.clean_disk()
            elif choice == 5:
                self.fixes.fix_network_issues()
            elif choice == 6:
                self.fixes.enhance_security()
            elif choice == 7:
                self.fixes.manage_startup()
            elif choice == 8:
                self.fixes.repair_system_files()

            input("\nНажмите Enter для продолжения...")

    def optimization_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.COLORS['info']}Раздел в разработке...")
        input("\nНажмите Enter для возврата в главное меню...")

    def real_time_monitor(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.COLORS['info']}Раздел в разработке...")
        input("\nНажмите Enter для возврата в главное меню...")

    def run(self):
        self.main_menu()