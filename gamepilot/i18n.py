"""i18n — internacionalização (EN/PT/ES/IT/RU)."""

import os
from enum import Enum, auto


class Language(Enum):
    ENGLISH = auto()
    PORTUGUESE = auto()
    SPANISH = auto()
    ITALIAN = auto()
    RUSSIAN = auto()


def get_language() -> Language:
    lang_env = os.environ.get("LANG", "en").lower()
    if lang_env.startswith("pt"):
        return Language.PORTUGUESE
    if lang_env.startswith("es"):
        return Language.SPANISH
    if lang_env.startswith("it"):
        return Language.ITALIAN
    if lang_env.startswith("ru"):
        return Language.RUSSIAN
    return Language.ENGLISH


# Dicionário de traduções
TRANSLATIONS: dict[str, dict[Language, str]] = {
    # Main UI
    "scan_games": {
        Language.ENGLISH: "Scan Games",
        Language.PORTUGUESE: "Escanear Jogos",
        Language.SPANISH: "Escanear Juegos",
        Language.ITALIAN: "Scansiona Giochi",
        Language.RUSSIAN: "Сканировать игры",
    },
    "dependencies_mods": {
        Language.ENGLISH: "Dependencies (Mods):",
        Language.PORTUGUESE: "Dependências (Mods):",
        Language.SPANISH: "Dependencias (Mods):",
        Language.ITALIAN: "Dipendenze (Mods):",
        Language.RUSSIAN: "Зависимости (Моды):",
    },
    "install_tool": {
        Language.ENGLISH: "Install Tool",
        Language.PORTUGUESE: "Instalar Ferramenta",
        Language.SPANISH: "Instalar Herramienta",
        Language.ITALIAN: "Installa Strumento",
        Language.RUSSIAN: "Установить инструмент",
    },
    "wine_tools": {
        Language.ENGLISH: "Wine Tools",
        Language.PORTUGUESE: "Ferramentas Wine",
        Language.SPANISH: "Herramientas Wine",
        Language.ITALIAN: "Strumenti Wine",
        Language.RUSSIAN: "Инструменты Wine",
    },
    "wine_prefix_placeholder": {
        Language.ENGLISH: "Wine prefix path (e.g. /home/user/.wine)",
        Language.PORTUGUESE: "Caminho do prefixo Wine (ex: /home/user/.wine)",
        Language.SPANISH: "Ruta del prefijo Wine (ej: /home/user/.wine)",
        Language.ITALIAN: "Percorso del prefisso Wine (es: /home/user/.wine)",
        Language.RUSSIAN: "Путь к префиксу Wine (напр. /home/user/.wine)",
    },
    "execute_wine_command": {
        Language.ENGLISH: "Execute Wine Command",
        Language.PORTUGUESE: "Executar Comando Wine",
        Language.SPANISH: "Ejecutar Comando Wine",
        Language.ITALIAN: "Esegui Comando Wine",
        Language.RUSSIAN: "Выполнить команду Wine",
    },
    # Status Messages
    "welcome": {
        Language.ENGLISH: "Welcome to GamePiLot!",
        Language.PORTUGUESE: "Bem-vindo ao GamePiLot!",
        Language.SPANISH: "¡Bienvenido a GamePiLot!",
        Language.ITALIAN: "Benvenuto in GamePiLot!",
        Language.RUSSIAN: "Добро пожаловать в GamePiLot!",
    },
    "no_games_scanned": {
        Language.ENGLISH: "No games scanned",
        Language.PORTUGUESE: "Nenhum jogo escaneado",
        Language.SPANISH: "Ningún juego escaneado",
        Language.ITALIAN: "Nessun gioco scansionato",
        Language.RUSSIAN: "Игры не отсканированы",
    },
    "no_game_selected": {
        Language.ENGLISH: "No game selected",
        Language.PORTUGUESE: "Nenhum jogo selecionado",
        Language.SPANISH: "Ningún juego seleccionado",
        Language.ITALIAN: "Nessun gioco selezionato",
        Language.RUSSIAN: "Игра не выбрана",
    },
    "no_games_found": {
        Language.ENGLISH: "No games found.",
        Language.PORTUGUESE: "Nenhum jogo encontrado.",
        Language.SPANISH: "No se encontraron juegos.",
        Language.ITALIAN: "Nessun gioco trovato.",
        Language.RUSSIAN: "Игры не найдены.",
    },
    "no_mod_manifest_found": {
        Language.ENGLISH: "No mod manifest found",
        Language.PORTUGUESE: "Nenhum manifesto de mod encontrado",
        Language.SPANISH: "No se encontró manifiesto de mod",
        Language.ITALIAN: "Nessun manifesto mod trovato",
        Language.RUSSIAN: "Манифест мода не найден",
    },
    "no_wine_prefix": {
        Language.ENGLISH: "❌ No Wine prefix detected! Select a game with prefix or fill field manually.",
        Language.PORTUGUESE: "❌ Nenhum prefixo Wine detectado! Selecione um jogo com prefixo ou preencha o campo manualmente.",
        Language.SPANISH: "❌ ¡No se detectó prefijo Wine! Selecciona un juego con prefijo o completa el campo manualmente.",
        Language.ITALIAN: "❌ Nessun prefisso Wine rilevato! Seleziona un gioco con un prefisso o compila il campo manualmente.",
        Language.RUSSIAN: "❌ Префикс Wine не обнаружен! Выберите игру с префиксом или введите путь вручную.",
    },
    "installing_dependencies": {
        Language.ENGLISH: "Installing dependencies...",
        Language.PORTUGUESE: "Instalando dependências...",
        Language.SPANISH: "Instalando dependencias...",
        Language.ITALIAN: "Installazione delle dipendenze...",
        Language.RUSSIAN: "Установка зависимостей...",
    },
    "preparing": {
        Language.ENGLISH: "Preparing...",
        Language.PORTUGUESE: "Preparando...",
        Language.SPANISH: "Preparando...",
        Language.ITALIAN: "Preparazione...",
        Language.RUSSIAN: "Подготовка...",
    },
    "dependencies_installed": {
        Language.ENGLISH: "Dependencies installed!",
        Language.PORTUGUESE: "Dependências instaladas!",
        Language.SPANISH: "¡Dependencias instaladas!",
        Language.ITALIAN: "Dipendenze installate!",
        Language.RUSSIAN: "Зависимости установлены!",
    },
    "done": {
        Language.ENGLISH: "🏁 Done.",
        Language.PORTUGUESE: "🏁 Concluído.",
        Language.SPANISH: "🏁 Terminado.",
        Language.ITALIAN: "🏁 Finito.",
        Language.RUSSIAN: "🏁 Готово.",
    },
    "enter_wine_prefix": {
        Language.ENGLISH: "Please, enter the Wine prefix path.",
        Language.PORTUGUESE: "Por favor, insira o caminho do prefixo Wine.",
        Language.SPANISH: "Por favor, introduzca la ruta del prefijo Wine.",
        Language.ITALIAN: "Si prega di inserire il percorso del prefisso Wine.",
        Language.RUSSIAN: "Пожалуйста, введите путь к префиксу Wine.",
    },
    "base_dependencies": {
        Language.ENGLISH: "📦 Installing base dependencies...",
        Language.PORTUGUESE: "📦 Instalando dependências base...",
        Language.SPANISH: "📦 Instalando dependencias base...",
        Language.ITALIAN: "📦 Installazione dipendenze di base...",
        Language.RUSSIAN: "📦 Установка базовых зависимостей...",
    },
    "running_installer": {
        Language.ENGLISH: "📦 Running tool installer...",
        Language.PORTUGUESE: "📦 Executando instalador da ferramenta...",
        Language.SPANISH: "📦 Ejecutando instalador de la herramienta...",
        Language.ITALIAN: "📦 Esecuzione del programma di installazione dello strumento...",
        Language.RUSSIAN: "📦 Запуск установщика инструмента...",
    },
    "setup_finished": {
        Language.ENGLISH: "✅ Tool setup finished.",
        Language.PORTUGUESE: "✅ Configuração da ferramenta concluída.",
        Language.SPANISH: "✅ Configuración de la herramienta completada.",
        Language.ITALIAN: "✅ Configurazione dello strumento completata.",
        Language.RUSSIAN: "✅ Настройка инструмента завершена.",
    },
    "finalizing": {
        Language.ENGLISH: "🏁 Finalizing setup...",
        Language.PORTUGUESE: "🏁 Finalizando configuração...",
        Language.SPANISH: "🏁 Finalizando configuración...",
        Language.ITALIAN: "🏁 Completamento configurazione...",
        Language.RUSSIAN: "🏁 Завершение настройки...",
    },
    "browse_prefix_tooltip": {
        Language.ENGLISH: "Choose the Wine prefix directory",
        Language.PORTUGUESE: "Escolher diretório do prefixo Wine",
        Language.SPANISH: "Elegir directorio del prefijo Wine",
        Language.ITALIAN: "Scegli la cartella del prefisso Wine",
        Language.RUSSIAN: "Выбрать каталог префикса Wine",
    },
    "select_wine_prefix": {
        Language.ENGLISH: "Select Wine prefix",
        Language.PORTUGUESE: "Selecionar prefixo Wine",
        Language.SPANISH: "Seleccionar prefijo Wine",
        Language.ITALIAN: "Seleziona prefisso Wine",
        Language.RUSSIAN: "Выбрать префикс Wine",
    },
    "confirm_close": {
        Language.ENGLISH: "There are operations in progress. Are you sure you want to close?",
        Language.PORTUGUESE: "Existem operações em andamento. Tem certeza que deseja fechar?",
        Language.SPANISH: "Hay operaciones en curso. ¿Está seguro de que desea cerrar?",
        Language.ITALIAN: "Ci sono operazioni in corso. Sei sicuro di voler chiudere?",
        Language.RUSSIAN: "Выполняются операции. Вы уверены, что хотите закрыть?",
    },
    # Nexus Mods
    "nexus_connect_prompt": {
        Language.ENGLISH: "To download automatically, connect your Nexus Mods account.",
        Language.PORTUGUESE: "Para baixar automaticamente, conecte sua conta do Nexus Mods.",
        Language.SPANISH: "Para descargar automáticamente, conecte su cuenta de Nexus Mods.",
        Language.ITALIAN: "Per scaricare automaticamente, collega il tuo account Nexus Mods.",
        Language.RUSSIAN: "Для автоматической загрузки подключите аккаунт Nexus Mods.",
    },
    "nexus_key_placeholder": {
        Language.ENGLISH: "Paste your free access key here",
        Language.PORTUGUESE: "Cole aqui sua chave de acesso gratuita",
        Language.SPANISH: "Pegue aquí su clave de acceso gratuita",
        Language.ITALIAN: "Incolla qui la tua chiave di accesso gratuita",
        Language.RUSSIAN: "Вставьте здесь свой бесплатный ключ доступа",
    },
    "nexus_connect": {
        Language.ENGLISH: "🔑 Connect",
        Language.PORTUGUESE: "🔑 Conectar",
        Language.SPANISH: "🔑 Conectar",
        Language.ITALIAN: "🔑 Connetti",
        Language.RUSSIAN: "🔑 Подключить",
    },
    "nexus_get_key": {
        Language.ENGLISH: "🌐 Get free key",
        Language.PORTUGUESE: "🌐 Obter chave gratuita",
        Language.SPANISH: "🌐 Obtener clave gratuita",
        Language.ITALIAN: "🌐 Ottieni chiave gratuita",
        Language.RUSSIAN: "🌐 Получить бесплатный ключ",
    },
    "nexus_connect_success": {
        Language.ENGLISH: "✅ Nexus Mods connected!",
        Language.PORTUGUESE: "✅ Nexus Mods conectado!",
        Language.SPANISH: "✅ ¡Nexus Mods conectado!",
        Language.ITALIAN: "✅ Nexus Mods connesso!",
        Language.RUSSIAN: "✅ Nexus Mods подключён!",
    },
    "nexus_key_invalid": {
        Language.ENGLISH: "Invalid key. Please check and try again.",
        Language.PORTUGUESE: "Chave inválida. Verifique e tente novamente.",
        Language.SPANISH: "Clave inválida. Verifique e inténtelo de nuevo.",
        Language.ITALIAN: "Chiave non valida. Verificare e riprovare.",
        Language.RUSSIAN: "Недействительный ключ. Проверьте и попробуйте снова.",
    },
    "nexus_no_internet": {
        Language.ENGLISH: "No internet connection.",
        Language.PORTUGUESE: "Sem conexão com a internet.",
        Language.SPANISH: "Sin conexión a internet.",
        Language.ITALIAN: "Nessuna connessione internet.",
        Language.RUSSIAN: "Нет подключения к интернету.",
    },
    "nexus_rate_limit": {
        Language.ENGLISH: "Too many attempts. Please wait and try again.",
        Language.PORTUGUESE: "Muitas tentativas. Aguarde um pouco e tente novamente.",
        Language.SPANISH: "Demasiados intentos. Espere un momento e inténtelo de nuevo.",
        Language.ITALIAN: "Troppi tentativi. Attendi un po' e riprova.",
        Language.RUSSIAN: "Слишком много попыток. Подождите и попробуйте снова.",
    },
    "nexus_mod_not_found": {
        Language.ENGLISH: "Tool not found on Nexus Mods.",
        Language.PORTUGUESE: "Ferramenta não encontrada no Nexus Mods.",
        Language.SPANISH: "Herramienta no encontrada en Nexus Mods.",
        Language.ITALIAN: "Strumento non trovato su Nexus Mods.",
        Language.RUSSIAN: "Инструмент не найден на Nexus Mods.",
    },
    "nexus_error_generic": {
        Language.ENGLISH: "Error connecting to Nexus Mods.",
        Language.PORTUGUESE: "Erro ao conectar ao Nexus Mods.",
        Language.SPANISH: "Error al conectarse a Nexus Mods.",
        Language.ITALIAN: "Errore di connessione a Nexus Mods.",
        Language.RUSSIAN: "Ошибка подключения к Nexus Mods.",
    },
    "nexus_downloading": {
        Language.ENGLISH: "⬇️ Downloading from Nexus Mods...",
        Language.PORTUGUESE: "⬇️ Baixando do Nexus Mods...",
        Language.SPANISH: "⬇️ Descargando de Nexus Mods...",
        Language.ITALIAN: "⬇️ Download da Nexus Mods...",
        Language.RUSSIAN: "⬇️ Загрузка с Nexus Mods...",
    },
    "nexus_already_connected": {
        Language.ENGLISH: "✅ Account connected",
        Language.PORTUGUESE: "✅ Conta conectada",
        Language.SPANISH: "✅ Cuenta conectada",
        Language.ITALIAN: "✅ Account connesso",
        Language.RUSSIAN: "✅ Аккаунт подключён",
    },
    "nexus_not_connected": {
        Language.ENGLISH: "Connect Nexus Mods account",
        Language.PORTUGUESE: "Conectar conta Nexus Mods",
        Language.SPANISH: "Conectar cuenta Nexus Mods",
        Language.ITALIAN: "Connetti account Nexus Mods",
        Language.RUSSIAN: "Подключить аккаунт Nexus Mods",
    },
    "nexus_connecting": {
        Language.ENGLISH: "Verifying key...",
        Language.PORTUGUESE: "Verificando chave...",
        Language.SPANISH: "Verificando clave...",
        Language.ITALIAN: "Verifica chiave...",
        Language.RUSSIAN: "Проверка ключа...",
    },
    "nexus_disconnect": {
        Language.ENGLISH: "Disconnect",
        Language.PORTUGUESE: "Desconectar",
        Language.SPANISH: "Desconectar",
        Language.ITALIAN: "Disconnetti",
        Language.RUSSIAN: "Отключить",
    },
    "nexus_invalid_response": {
        Language.ENGLISH: "Invalid response from Nexus Mods.",
        Language.PORTUGUESE: "Resposta inválida do Nexus Mods.",
        Language.SPANISH: "Respuesta inválida de Nexus Mods.",
        Language.ITALIAN: "Risposta non valida da Nexus Mods.",
        Language.RUSSIAN: "Неверный ответ от Nexus Mods.",
    },
    "nexus_no_files": {
        Language.ENGLISH: "No files found for this mod.",
        Language.PORTUGUESE: "Nenhum arquivo encontrado para este mod.",
        Language.SPANISH: "No se encontraron archivos para este mod.",
        Language.ITALIAN: "Nessun file trovato per questo mod.",
        Language.RUSSIAN: "Файлы для этого мода не найдены.",
    },
    "nexus_invalid_file_id": {
        Language.ENGLISH: "Invalid file ID.",
        Language.PORTUGUESE: "ID de arquivo inválido.",
        Language.SPANISH: "ID de archivo inválido.",
        Language.ITALIAN: "ID file non valido.",
        Language.RUSSIAN: "Неверный идентификатор файла.",
    },
    "nexus_no_download_link": {
        Language.ENGLISH: "Download link not found.",
        Language.PORTUGUESE: "Link de download não encontrado.",
        Language.SPANISH: "Enlace de descarga no encontrado.",
        Language.ITALIAN: "Link di download non trovato.",
        Language.RUSSIAN: "Ссылка для скачивания не найдена.",
    },
    "nexus_free_tier_download": {
        Language.ENGLISH: "API download requires Premium. Open the mod in the browser.",
        Language.PORTUGUESE: "Download via API requer Premium. Abra o mod no navegador.",
        Language.SPANISH: "La descarga vía API requiere Premium. Abra el mod en el navegador.",
        Language.ITALIAN: "Il download via API richiede Premium. Apri il mod nel browser.",
        Language.RUSSIAN: "Скачивание через API требует Premium. Откройте мод в браузере.",
    },
    "install_delegated_browser": {
        Language.ENGLISH: "🌐 Mod opened in the browser. Download and install manually.",
        Language.PORTUGUESE: "🌐 Mod aberto no navegador. Baixe e instale manualmente.",
        Language.SPANISH: "🌐 Mod abierto en el navegador. Descárgalo e instálalo manualmente.",
        Language.ITALIAN: "🌐 Mod aperto nel browser. Scaricalo e installalo manualmente.",
        Language.RUSSIAN: "🌐 Мод открыт в браузере. Скачайте и установите вручную.",
    },
    "install_failed": {
        Language.ENGLISH: "❌ Installation failed.",
        Language.PORTUGUESE: "❌ Falha na instalação.",
        Language.SPANISH: "❌ Falló la instalación.",
        Language.ITALIAN: "❌ Installazione fallita.",
        Language.RUSSIAN: "❌ Установка не удалась.",
    },
    # Helper strings with formatting
    "t_downloading": {
        Language.ENGLISH: "📦 Downloading {}...",
        Language.PORTUGUESE: "📦 Baixando {}...",
        Language.SPANISH: "📦 Descargando {}...",
        Language.ITALIAN: "📦 Download di {}...",
        Language.RUSSIAN: "📦 Загрузка {}...",
    },
    "t_failed_download": {
        Language.ENGLISH: "❌ Failed to download {}",
        Language.PORTUGUESE: "❌ Falha no download de {}",
        Language.SPANISH: "❌ Error al descargar {}",
        Language.ITALIAN: "❌ Download di {} non riuscito",
        Language.RUSSIAN: "❌ Ошибка загрузки {}",
    },
    "t_installing_via_winetricks": {
        Language.ENGLISH: "📦 Installing {} via winetricks...",
        Language.PORTUGUESE: "📦 Instalando {} via winetricks...",
        Language.SPANISH: "📦 Instalando {} a través de winetricks...",
        Language.ITALIAN: "📦 Installazione di {} tramite winetricks...",
        Language.RUSSIAN: "📦 Установка {} через winetricks...",
    },
    "t_failed_install": {
        Language.ENGLISH: "❌ Failed to install {}: {}",
        Language.PORTUGUESE: "❌ Falha ao instalar {}: {}",
        Language.SPANISH: "❌ Error al instalar {}: {}",
        Language.ITALIAN: "❌ Impossibile installare {}: {}",
        Language.RUSSIAN: "❌ Ошибка при установке {}: {}",
    },
    "t_install_failed": {
        Language.ENGLISH: "❌ Installation failed: {}",
        Language.PORTUGUESE: "❌ Falha na instalação: {}",
        Language.SPANISH: "❌ Falló la instalación: {}",
        Language.ITALIAN: "❌ Installazione fallita: {}",
        Language.RUSSIAN: "❌ Установка не удалась: {}",
    },
    "t_redirecting_browser": {
        Language.ENGLISH: "🌐 Redirecting to browser for manual download...",
        Language.PORTUGUESE: "🌐 Redirecionando para o navegador para download manual...",
        Language.SPANISH: "🌐 Redirigiendo al navegador para descarga manual...",
        Language.ITALIAN: "🌐 Reindirizzamento al browser per il download manuale...",
        Language.RUSSIAN: "🌐 Перенаправление в браузер для ручной загрузки...",
    },
    "launch_tool": {
        Language.ENGLISH: "🚀 Launch Tool",
        Language.PORTUGUESE: "🚀 Lançar Ferramenta",
        Language.SPANISH: "🚀 Lanzar Herramienta",
        Language.ITALIAN: "🚀 Avvia Strumento",
        Language.RUSSIAN: "🚀 Запустить инструмент",
    },
    "tool_launched": {
        Language.ENGLISH: "Tool launched! 🚀",
        Language.PORTUGUESE: "Ferramenta lançada! 🚀",
        Language.SPANISH: "¡Herramienta lanzada! 🚀",
        Language.ITALIAN: "Strumento avviato! 🚀",
        Language.RUSSIAN: "Инструмент запущен! 🚀",
    },
    "launch_failed": {
        Language.ENGLISH: "❌ Failed to launch tool: {}",
        Language.PORTUGUESE: "❌ Erro ao lançar ferramenta: {}",
        Language.SPANISH: "❌ Error al lanzar herramienta: {}",
        Language.ITALIAN: "❌ Impossibile avviare strumento: {}",
        Language.RUSSIAN: "❌ Не удалось запустить инструмент: {}",
    },
    "shortcut_created": {
        Language.ENGLISH: "✅ Desktop shortcut created!",
        Language.PORTUGUESE: "✅ Atalho de área de trabalho criado!",
        Language.SPANISH: "✅ ¡Acceso directo al escritorio creado!",
        Language.ITALIAN: "✅ Collegamento sul desktop creato!",
        Language.RUSSIAN: "✅ Ярлык на рабочем столе создан!",
    },
    "shortcut_failed": {
        Language.ENGLISH: "❌ Failed to create shortcut: {}",
        Language.PORTUGUESE: "❌ Falha ao criar atalho: {}",
        Language.SPANISH: "❌ Error al crear acceso directo: {}",
        Language.ITALIAN: "❌ Impossibile creare collegamento: {}",
        Language.RUSSIAN: "❌ Не удалось создать ярлык: {}",
    },
    "missing_system_deps": {
        Language.ENGLISH: "⚠️ Missing system dependencies: {}. Install them first.",
        Language.PORTUGUESE: "⚠️ Ferramentas não encontradas: {}. Instale antes de usar.",
        Language.SPANISH: "⚠️ Herramientas no encontradas: {}. Instálelas antes de usar.",
        Language.ITALIAN: "⚠️ Strumenti non trovati: {}. Installare prima dell'uso.",
        Language.RUSSIAN: "⚠️ Инструменты не найдены: {}. Установите их перед использованием.",
    },
}


def t(key: str) -> str:
    """Traduz chave para o idioma atual."""
    lang = get_language()
    entry = TRANSLATIONS.get(key)
    if entry:
        return entry.get(lang, entry.get(Language.ENGLISH, key))
    return key


def t_fmt(key: str, *args) -> str:
    """Traduz e formata com args."""
    return t(key).format(*args)
