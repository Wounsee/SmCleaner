import os
import platform
import psutil
import cpuinfo
import subprocess
import winreg
from datetime import datetime
from .utils import format_size, get_color, print_progress_bar, print_section


class SystemDiagnostics:
    def __init__(self):
        pass

    def general_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ОБЩАЯ ИНФОРМАЦИЯ О СИСТЕМЕ", "cyan")


        print(f"{'Операционная система:':<25} {platform.system()} {platform.release()} ({platform.architecture()[0]})")
        print(f"{'Версия ОС:':<25} {platform.version()}")
        print(f"{'Имя компьютера:':<25} {platform.node()}")
        print(f"{'Имя пользователя:':<25} {os.getlogin()}")
        print(f"{'Дата и время:':<25} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        print(f"{'Время работы:':<25} {str(uptime).split('.')[0]}")


        cpu_info = cpuinfo.get_cpu_info()
        print(f"{'Процессор:':<25} {cpu_info['brand_raw']}")
        print(f"{'Ядра/потоки:':<25} {psutil.cpu_count(logical=False)}/{psutil.cpu_count()}")


        mem = psutil.virtual_memory()
        print(f"{'Оперативная память:':<25} {format_size(mem.total)}")


        partitions = psutil.disk_partitions()
        print(f"{'Дисковые разделы:':<25} {len(partitions)}")

    def components_status(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("СТАТУС КОМПОНЕНТОВ СИСТЕМЫ", "magenta")


        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_color = get_color(cpu_usage, [70, 90])
        print(f"{'Процессор:':<20} {cpu_color}{cpu_usage}%{' ' * 10}{print_progress_bar(cpu_usage)}")


        mem = psutil.virtual_memory()
        ram_color = get_color(mem.percent, [75, 85])
        print(f"{'Оперативная память:':<20} {ram_color}{mem.percent}%{' ' * 10}{print_progress_bar(mem.percent)}")


        for part in psutil.disk_partitions():
            if 'cdrom' in part.opts or part.fstype == '':
                continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_color = get_color(usage.percent, [80, 90])
            print(
                f"{'Диск ' + part.device + ':':<20} {disk_color}{usage.percent}%{' ' * 10}{print_progress_bar(usage.percent)}")


        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                core_temp = max([t.current for t in temps['coretemp']])
                temp_color = get_color(core_temp, [70, 80])
                print(f"{'Температура CPU:':<20} {temp_color}{core_temp}°C")
        except:
            print(f"{'Температура CPU:':<20} Недоступна")


        try:
            battery = psutil.sensors_battery()
            if battery:
                bat_color = "green" if battery.percent > 30 else "yellow" if battery.percent > 10 else "red"
                print(f"{'Батарея:':<20} {bat_color}{battery.percent}%")
        except:
            pass

    def cpu_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ПРОЦЕССОРЕ", "yellow")


        cpu_info = cpuinfo.get_cpu_info()


        print(f"{'Производитель:':<20} {cpu_info['vendor_id_raw']}")
        print(f"{'Модель:':<20} {cpu_info['brand_raw']}")
        print(f"{'Архитектура:':<20} {cpu_info['arch']}")
        print(f"{'Тактовая частота:':<20} {psutil.cpu_freq().current:.2f} МГц")
        print(f"{'Ядра (физические/логические):':<20} {psutil.cpu_count(logical=False)}/{psutil.cpu_count()}")


        print("\nЗАГРУЗКА ПРОЦЕССОРА:")
        for i, perc in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
            print(f"  Ядро {i + 1}: {print_progress_bar(perc)} {perc}%")


        if 'l3_cache_size' in cpu_info:
            print(f"\n{'Кэш L3:':<20} {cpu_info['l3_cache_size'] // 1024} MB")
        if 'l2_cache_size' in cpu_info:
            print(f"{'Кэш L2:':<20} {cpu_info['l2_cache_size'] // 1024} MB")
        if 'l1_cache_size' in cpu_info:
            print(f"{'Кэш L1:':<20} {cpu_info['l1_cache_size'] // 1024} MB")

    def ram_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ИНФОРМАЦИЯ ОБ ОПЕРАТИВНОЙ ПАМЯТИ", "yellow")

        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        print(f"{'Всего памяти:':<20} {format_size(mem.total)}")
        print(f"{'Использовано:':<20} {format_size(mem.used)} ({mem.percent}%)")
        print(f"{'Доступно:':<20} {format_size(mem.available)}")
        print(f"{'Своп:':<20} {format_size(swap.used)} из {format_size(swap.total)}")

    def disks_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ДИСКИ И НАКОПИТЕЛИ", "yellow")

        for part in psutil.disk_partitions():
            if 'cdrom' in part.opts or part.fstype == '':
                continue

            usage = psutil.disk_usage(part.mountpoint)
            print(f"\n{part.device} ({part.fstype}) @ {part.mountpoint}")
            print(f"{'Всего:':<10} {format_size(usage.total)}")
            print(f"{'Использовано:':<10} {format_size(usage.used)}")
            print(f"{'Свободно:':<10} {format_size(usage.free)}")
            print(f"{'Использование:':<10} {print_progress_bar(usage.percent)} {usage.percent}%")

    def network_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("СЕТЬ И ИНТЕРНЕТ", "yellow")

        net_io = psutil.net_io_counters()
        print(f"{'Отправлено:':<15} {format_size(net_io.bytes_sent)}")
        print(f"{'Получено:':<15} {format_size(net_io.bytes_recv)}")
        print(f"{'Ошибки:':<15} {net_io.errin + net_io.errout}")

        print("\nАктивные соединения:")
        for conn in psutil.net_connections(kind='inet')[:5]:
            if conn.laddr and conn.raddr:
                print(f"  {conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port} ({conn.status})")

    def security_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ДИАГНОСТИКА БЕЗОПАСНОСТИ", "red")

        risks = []
        security_level = "Высокий"
        color = "green"


        try:
            if platform.system() == "Windows":
                result = subprocess.check_output('netsh advfirewall show allprofiles state', shell=True)
                if b"OFF" in result:
                    risks.append("Брандмауэр отключен")
                    security_level = "Низкий"
                    color = "red"
        except:
            pass


        try:
            if platform.system() == "Windows":
                av_running = False
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'].lower() in ['msmpeng.exe', 'avp.exe', 'bdagent.exe']:
                        av_running = True
                if not av_running:
                    risks.append("Антивирус не запущен")
                    security_level = "Низкий"
                    color = "red"
        except:
            pass


        try:
            if platform.system() == "Windows":
                update_session = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update"
                )
                last_update, _ = winreg.QueryValueEx(update_session, "LastInstallSuccessTime")
                if (datetime.now() - datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")).days > 30:
                    risks.append("Обновления ОС не устанавливались более 30 дней")
                    security_level = "Средний"
                    color = "yellow"
        except:
            pass


        dangerous_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 389, 443, 445, 3389]
        open_ports = []
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and conn.laddr.port in dangerous_ports:
                open_ports.append(conn.laddr.port)

        if open_ports:
            risks.append(f"Открыты опасные порты: {', '.join(map(str, set(open_ports)))}")
            security_level = "Низкий"
            color = ""


            print(f"Уровень безопасности: {color}{security_level}")

            if risks:
                print("\nОБНАРУЖЕНЫ РИСКИ БЕЗОПАСНОСТИ:")
            for risk in risks:
                print(f"  [!] {risk}")
            else:
                print("\n[+] Критических проблем с безопасностью не обнаружено")


            print("\nРЕКОМЕНДАЦИИ:")
            if "Брандмауэр отключен" in risks:
                print("  - Включите брандмауэр Windows")
            if "Антивирус не запущен" in risks:
                print("  - Установите и включите антивирусное ПО")
            if "Обновления ОС не устанавливались" in risks:
                print("  - Проверьте обновления Windows")
            if "Открыты опасные порты" in risks:
                print("  - Используйте раздел 'Решение проблем' для закрытия портов")
            else:
                print("У вас все хорошо!")

    def processes_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("ПРОЦЕССЫ И СЛУЖБЫ", "yellow")

        print("Топ процессов по использованию CPU:")
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except psutil.NoSuchProcess:
                continue


        processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:10]

        for i, proc in enumerate(processes):
            print(
                f"{i + 1}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']}%, RAM: {proc['memory_percent']:.1f}%")

    def sensors_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_section("АППАРАТНЫЕ ДАТЧИКИ", "yellow")

        try:

            temps = psutil.sensors_temperatures()
            if temps:
                print("Температуры:")
                for name, entries in temps.items():
                    for entry in entries:
                        print(f"  {entry.label or name}: {entry.current}°C")


            fans = psutil.sensors_fans()
            if fans:
                print("\nВентиляторы:")
                for name, entries in fans.items():
                    for entry in entries:
                        print(f"  {entry.label or name}: {entry.current} RPM")
        except:
            print("Данные с датчиков недоступны")

    def full_report(self):
        import time
        os.system('cls' if os.name == 'nt' else 'clear')
        self.general_info()
        time.sleep(10)
        self.components_status()
        time.sleep(10)
        self.cpu_info()
        time.sleep(10)
        self.ram_info()
        time.sleep(10)
        self.disks_info()
        time.sleep(10)
        self.network_info()
        time.sleep(10)
        self.security_info()
        time.sleep(10)
        self.processes_info()
        time.sleep(10)
        self.sensors_info()
        time.sleep(0.1)