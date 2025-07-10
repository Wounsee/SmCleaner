import os
import subprocess
import psutil
import platform
import ctypes
import winreg
import shutil
import time
from colorama import Fore, Style
from .utils import print_section, run_as_admin


class SystemFixes:
    def close_dangerous_ports(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ЗАКРЫТИЕ ОПАСНЫХ ПОРТОВ", "red")

        ports_to_block = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 389, 443, 445, 3389]

        if not run_as_admin():
            print(f"{Fore.RED}Требуются права администратора!{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}[+] Блокировка опасных портов...{Style.RESET_ALL}")


        try:
            subprocess.run(
                'powershell -Command "Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart"',
                shell=True,
                check=True
            )
            print(f"{Fore.GREEN}[+] SMBv1 отключен{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Ошибка при отключении SMBv1{Style.RESET_ALL}")


        try:
            subprocess.run(
                'netsh interface ipv4 set interface * nettbios=disable',
                shell=True,
                check=True
            )
            print(f"{Fore.GREEN}[+] NetBIOS отключен{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Ошибка при отключении NetBIOS{Style.RESET_ALL}")


        for port in ports_to_block:
            try:

                subprocess.run(
                    f'netsh advfirewall firewall add rule name="BLOCK PORT {port} IN" '
                    f'dir=in action=block protocol=TCP localport={port}',
                    shell=True,
                    check=True
                )


                subprocess.run(
                    f'netsh advfirewall firewall add rule name="BLOCK PORT {port} OUT" '
                    f'dir=out action=block protocol=TCP localport={port}',
                    shell=True,
                    check=True
                )
                print(f"{Fore.GREEN}[+] Порт {port} заблокирован{Style.RESET_ALL}")
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}[!] Ошибка при блокировке порта {port}{Style.RESET_ALL}")


        try:
            subprocess.run('sc config RpcSs start= disabled', shell=True, check=True)
            subprocess.run('net stop RpcSs', shell=True)
            print(f"{Fore.GREEN}[+] Служба RPC отключена{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Ошибка при отключении RPC{Style.RESET_ALL}")


        try:
            subprocess.run('sc config W3SVC start= disabled', shell=True, check=True)
            subprocess.run('net stop W3SVC', shell=True)
            print(f"{Fore.GREEN}[+] HTTP-сервер отключен{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!] Ошибка при отключении HTTP-сервера{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}[+] Все опасные порты закрыты!{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}[!] Для полного применения изменений может потребоваться перезагрузка системы{Style.RESET_ALL}")

    def optimize_cpu(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ОПТИМИЗАЦИЯ РАБОТЫ ПРОЦЕССОРА", "yellow")

        if not run_as_admin():
            print(f"{Fore.RED}Требуются права администратора!{Style.RESET_ALL}")
            return

        try:

            print(f"{Fore.YELLOW}[+] Настраиваю схему электропитания...{Style.RESET_ALL}")
            subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True, check=True)


            print(f"{Fore.YELLOW}[+] Оптимизирую приоритеты процессов...{Style.RESET_ALL}")
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] in ['svchost.exe', 'explorer.exe']:
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                    except:
                        pass


            print(f"{Fore.YELLOW}[+] Очищаю кэш DNS...{Style.RESET_ALL}")
            subprocess.run('ipconfig /flushdns', shell=True, check=True)


            services_to_disable = [
                "SysMain",
                "DiagTrack",
                "WSearch"
            ]

            for service in services_to_disable:
                try:
                    print(f"{Fore.YELLOW}[+] Отключаю службу {service}...{Style.RESET_ALL}")
                    subprocess.run(f'sc stop "{service}"', shell=True)
                    subprocess.run(f'sc config "{service}" start= disabled', shell=True, check=True)
                except:
                    print(f"{Fore.RED}[!] Не удалось отключить службу {service}{Style.RESET_ALL}")

            print(f"\n{Fore.GREEN}[+] Оптимизация процессора завершена!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[!] Рекомендуется перезапустить систему для применения изменений{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка оптимизации: {str(e)}{Style.RESET_ALL}")

    def free_up_ram(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ОСВОБОЖДЕНИЕ ОПЕРАТИВНОЙ ПАМЯТИ", "magenta")

        try:

            print(f"{Fore.YELLOW}[+] Поиск процессов с высоким потреблением памяти...{Style.RESET_ALL}")
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    if proc.info['memory_percent'] > 1.0:
                        processes.append(proc.info)
                except:
                    pass


            processes = sorted(processes, key=lambda p: p['memory_percent'], reverse=True)

            if not processes:
                print(f"{Fore.GREEN}[+] Нет процессов с высоким потреблением памяти{Style.RESET_ALL}")
                return


            print(f"\n{Fore.CYAN}Процессы с высоким потреблением памяти:{Style.RESET_ALL}")
            for i, proc in enumerate(processes[:10]):
                print(f"{i + 1}. {proc['name']} (PID: {proc['pid']}) - {proc['memory_percent']:.1f}%")

            print(
                f"\n{Fore.YELLOW}Введите номера процессов для завершения (через пробел), или 0 для отмены:{Style.RESET_ALL}")
            choices = input(">>> ").split()

            if "0" in choices:
                print(f"{Fore.YELLOW}[-] Отмена операции{Style.RESET_ALL}")
                return


            for choice in choices:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(processes):
                        pid = processes[index]['pid']
                        p = psutil.Process(pid)
                        p.terminate()
                        print(f"{Fore.GREEN}[+] Процесс {p.name()} (PID: {pid}) завершен{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{Fore.RED}[!] Неверный номер: {choice}{Style.RESET_ALL}")
                except psutil.AccessDenied:
                    print(f"{Fore.RED}[!] Нет прав для завершения процесса {processes[index]['name']}{Style.RESET_ALL}")
                except psutil.NoSuchProcess:
                    print(f"{Fore.RED}[!] Процесс уже завершен{Style.RESET_ALL}")


            if platform.system() == "Windows":
                print(f"{Fore.YELLOW}[+] Очищаю кэш памяти...{Style.RESET_ALL}")
                ctypes.windll.psapi.EmptyWorkingSet(ctypes.c_ulong(-1))


            mem = psutil.virtual_memory()
            print(f"\n{Fore.GREEN}[+] Освобождено памяти!{Style.RESET_ALL}")
            print(
                f"{Fore.CYAN}Доступно памяти: {format_size(mem.available)} ({mem.percent}% использовано){Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка: {str(e)}{Style.RESET_ALL}")

    def clean_disk(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ОЧИСТКА ДИСКА ОТ МУСОРА", "cyan")

        if not run_as_admin():
            print(f"{Fore.RED}Требуются права администратора!{Style.RESET_ALL}")
            return

        try:

            print(f"{Fore.YELLOW}[+] Очищаю временные файлы...{Style.RESET_ALL}")
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                r'C:\Windows\Temp',
                r'C:\Windows\Prefetch'
            ]

            total_freed = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for filename in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, filename)
                        try:
                            if os.path.isfile(file_path):
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                total_freed += file_size
                        except:
                            pass


            print(f"{Fore.YELLOW}[+] Очищаю кэш браузеров...{Style.RESET_ALL}")
            browsers = [
                os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
                os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
                os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles')
            ]

            for cache_dir in browsers:
                if os.path.exists(cache_dir):
                    shutil.rmtree(cache_dir, ignore_errors=True)


            print(f"{Fore.YELLOW}[+] Очищаю корзину...{Style.RESET_ALL}")
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            except:
                pass


            print(f"{Fore.YELLOW}[+] Очищаю старые обновления Windows...{Style.RESET_ALL}")
            subprocess.run('Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase', shell=True)

            print(f"\n{Fore.GREEN}[+] Очистка диска завершена!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[!] Освобождено: {format_size(total_freed)}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка очистки диска: {str(e)}{Style.RESET_ALL}")

    def fix_network_issues(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ИСПРАВЛЕНИЕ СЕТЕВЫХ ПРОБЛЕМ", "blue")

        if not run_as_admin():
            print(f"{Fore.RED}Требуются права администратора!{Style.RESET_ALL}")
            return

        try:
            print(f"{Fore.YELLOW}[+] Сбрасываю сетевые настройки...{Style.RESET_ALL}")
            subprocess.run('netsh winsock reset', shell=True, check=True)
            subprocess.run('netsh int ip reset', shell=True, check=True)
            subprocess.run('ipconfig /release', shell=True, check=True)

            print(f"{Fore.YELLOW}[+] Обновляю IP-адрес...{Style.RESET_ALL}")
            subprocess.run('ipconfig /renew', shell=True, check=True)

            print(f"{Fore.YELLOW}[+] Очищаю кэш DNS...{Style.RESET_ALL}")
            subprocess.run('ipconfig /flushdns', shell=True, check=True)

            print(f"{Fore.YELLOW}[+] Сбрасываю кэш маршрутизации...{Style.RESET_ALL}")
            subprocess.run('route /f', shell=True, check=True)

            print(f"\n{Fore.GREEN}[+] Сетевые проблемы исправлены!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[!] Рекомендуется перезагрузить компьютер{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка исправления сетевых проблем: {str(e)}{Style.RESET_ALL}")

    def enhance_security(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ПОВЫШЕНИЕ БЕЗОПАСНОСТИ СИСТЕМЫ", "red")

        if not run_as_admin():
            print(f"{Fore.RED}Требуются права администратора!{Style.RESET_ALL}")
            return

        try:

            print(f"{Fore.YELLOW}[+] Включаю брандмауэр...{Style.RESET_ALL}")
            subprocess.run('netsh advfirewall set allprofiles state on', shell=True, check=True)


            print(f"{Fore.YELLOW}[+] Настраиваю контроль учетных записей (UAC)...{Style.RESET_ALL}")
            subprocess.run(
                'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" '
                '/v EnableLUA /t REG_DWORD /d 1 /f', shell=True, check=True
            )


            print(f"{Fore.YELLOW}[+] Отключаю автозапуск со съемных носителей...{Style.RESET_ALL}")
            subprocess.run(
                'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" '
                '/v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f', shell=True, check=True
            )


            insecure_services = [
                "SSDPSRV",
                "upnphost",
                "RemoteRegistry"
            ]

            for service in insecure_services:
                try:
                    print(f"{Fore.YELLOW}[+] Отключаю службу {service}...{Style.RESET_ALL}")
                    subprocess.run(f'sc stop "{service}"', shell=True)
                    subprocess.run(f'sc config "{service}" start= disabled', shell=True, check=True)
                except:
                    print(f"{Fore.RED}[!] Не удалось отключить службу {service}{Style.RESET_ALL}")


            print(f"{Fore.YELLOW}[+] Устанавливаю политику сложных паролей...{Style.RESET_ALL}")
            subprocess.run(
                'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" '
                '/v NoLMHash /t REG_DWORD /d 1 /f', shell=True, check=True
            )

            print(f"\n{Fore.GREEN}[+] Безопасность системы повышена!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[!] Рекомендуется установить антивирусное ПО{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка повышения безопасности: {str(e)}{Style.RESET_ALL}")

    def manage_startup(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("УПРАВЛЕНИЕ АВТОЗАГРУЗКОЙ", "magenta")

        try:

            print(f"{Fore.YELLOW}[+] Получаю список программ в автозагрузке...{Style.RESET_ALL}")
            startup_path = os.path.join(os.environ['APPDATA'],
                                        'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            common_startup = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'

            startup_items = []


            if os.path.exists(startup_path):
                for item in os.listdir(startup_path):
                    if item.endswith('.lnk') or item.endswith('.exe'):
                        startup_items.append({
                            'name': os.path.splitext(item)[0],
                            'path': os.path.join(startup_path, item),
                            'type': 'user'
                        })


            if os.path.exists(common_startup):
                for item in os.listdir(common_startup):
                    if item.endswith('.lnk') or item.endswith('.exe'):
                        startup_items.append({
                            'name': os.path.splitext(item)[0],
                            'path': os.path.join(common_startup, item),
                            'type': 'common'
                        })


            try:
                reg_paths = [
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
                    r"Software\Microsoft\Windows\CurrentVersion\RunServices"
                ]

                hives = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]

                for hive in hives:
                    for path in reg_paths:
                        try:
                            with winreg.OpenKey(hive, path) as key:
                                index = 0
                                while True:
                                    try:
                                        name, value, _ = winreg.EnumValue(key, index)
                                        startup_items.append({
                                            'name': name,
                                            'path': value,
                                            'type': 'registry'
                                        })
                                        index += 1
                                    except OSError:
                                        break
                        except FileNotFoundError:
                            pass
            except:
                pass

            if not startup_items:
                print(f"{Fore.GREEN}[-] Нет программ в автозагрузке{Style.RESET_ALL}")
                return


            print(f"\n{Fore.CYAN}Программы в автозагрузке:{Style.RESET_ALL}")
            for i, item in enumerate(startup_items):
                print(f"{i + 1}. [{item['type']}] {item['name']}")

            print(
                f"\n{Fore.YELLOW}Введите номера программ для удаления из автозагрузки (через пробел), или 0 для отмены:{Style.RESET_ALL}")
            choices = input(">>> ").split()

            if "0" in choices:
                print(f"{Fore.YELLOW}[-] Отмена операции{Style.RESET_ALL}")
                return


            for choice in choices:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(startup_items):
                        item = startup_items[index]

                        if item['type'] == 'user' or item['type'] == 'common':
                            try:
                                os.remove(item['path'])
                                print(f"{Fore.GREEN}[+] Удален файл: {item['name']}{Style.RESET_ALL}")
                            except:
                                print(f"{Fore.RED}[!] Не удалось удалить файл: {item['name']}{Style.RESET_ALL}")

                        elif item['type'] == 'registry':
                            hive = winreg.HKEY_CURRENT_USER if "CurrentVersion" in item[
                                'path'] else winreg.HKEY_LOCAL_MACHINE
                            reg_path = item['path'].split('\\', 1)[1]

                            try:
                                with winreg.OpenKey(hive, reg_path, 0, winreg.KEY_WRITE) as key:
                                    winreg.DeleteValue(key, item['name'])
                                print(f"{Fore.GREEN}[+] Удалена запись реестра: {item['name']}{Style.RESET_ALL}")
                            except:
                                print(f"{Fore.RED}[!] Не удалось удалить запись реестра: {item['name']}{Style.RESET_ALL}")
                except (ValueError, IndexError):
                    print(f"{Fore.RED}[!] Неверный номер: {choice}{Style.RESET_ALL}")

            print(f"\n{Fore.GREEN}[+] Управление автозагрузкой завершено!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[!] Изменения вступят в силу после перезагрузки{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка: {str(e)}{Style.RESET_ALL}")

    def repair_system_files(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ВОССТАНОВЛЕНИЕ СИСТЕМНЫХ ФАЙЛОВ", "green")

        if not run_as_admin():
            print(f"{Fore.RED}Требуются права администратора!{Style.RESET_ALL}")
            return

        try:
            print(f"{Fore.YELLOW}[+] Проверяю целостность системных файлов...{Style.RESET_ALL}")
            result = subprocess.run('sfc /scannow', shell=True, capture_output=True, text=True)

            if "нарушения целостности" in result.stdout:
                print(f"{Fore.RED}[!] Обнаружены поврежденные системные файлы!{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Нарушений целостности не обнаружено{Style.RESET_ALL}")

            print(f"\n{Fore.YELLOW}[+] Восстанавливаю системные файлы...{Style.RESET_ALL}")
            subprocess.run('dism /online /cleanup-image /restorehealth', shell=True, check=True)

            print(f"\n{Fore.GREEN}[+] Восстановление завершено!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[!] Рекомендуется перезагрузить компьютер{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[-] Ошибка восстановления: {str(e)}{Style.RESET_ALL}")



def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"