document.addEventListener('DOMContentLoaded', function () {
    // Exibe mensagem sobre o registro se for um novo dia
    const messageElement = document.getElementById('message');

    if (messageElement) {
        const isNewDay = messageElement.dataset.newDay === 'true';

        if (isNewDay) {
            displayNewDayMessage(messageElement);
        } else {
            messageElement.textContent = '';
        }
    }

    // Ciclo de registros
    const registrationTypes = ['entrada', 'pausa', 'retorno', 'saida'];
    let currentIndex = 0;

    const button = document.getElementById('registrar-button');
    const tipoRegistroInput = document.getElementById('tipo_registro');

    if (button && tipoRegistroInput) {
        button.addEventListener('click', function (event) {
            handleRegistrationClick();
        });
    }

    // Inicia o relógio assim que a página é carregada
    startClock();

    /**
     * Funções Auxiliares
     */

    // Exibe a mensagem de novo dia
    function displayNewDayMessage(element) {
        element.textContent = 'Novo dia! Registros foram reiniciados.';
        element.classList.add('text-blue-600');
    }

    // Lida com o clique no botão de registro
    function handleRegistrationClick() {
        const clockElement = document.getElementById('clock');
        if (!clockElement) return;

        const horaRegistro = clockElement.textContent;
        tipoRegistroInput.value = registrationTypes[currentIndex];
        document.getElementById('hora_registro').value = horaRegistro;

        // Atualiza o texto do botão conforme o próximo tipo de registro
        currentIndex = (currentIndex + 1) % registrationTypes.length;
        button.textContent = `Registrar ${capitalizeFirstLetter(registrationTypes[currentIndex])}`;
    }

    // Capitaliza a primeira letra de uma string
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Inicia o relógio e o atualiza a cada segundo
    function startClock() {
        function updateClock() {
            const clockElement = document.getElementById('clock');
            if (!clockElement) return;

            const now = new Date();
            clockElement.textContent = formatTime(now);
        }

        // Formata o tempo em HH:MM:SS
        function formatTime(date) {
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');
            return `${hours}:${minutes}:${seconds}`;
        }

        // Atualiza o relógio a cada segundo
        setInterval(updateClock, 1000);
        updateClock(); // Atualiza imediatamente ao carregar a página
    }
});
