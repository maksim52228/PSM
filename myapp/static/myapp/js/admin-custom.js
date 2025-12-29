// admin-custom.js – кастомный JavaScript для красивой админки Django (Jazzmin)

document.addEventListener('DOMContentLoaded', function () {

    // 1. Автофокус на первое поле при добавлении объекта
    if (window.location.pathname.includes('/add/')) {
        const firstInput = document.querySelector(
            'input[type="text"]:not([readonly]):not(:disabled), ' +
            'input[type="email"]:not([readonly]):not(:disabled), ' +
            'input[type="number"]:not([readonly]):not(:disabled), ' +
            'textarea:not([readonly]):not(:disabled), ' +
            'select:not([readonly]):not(:disabled)'
        );
        if (firstOfAll && firstInput) {
            firstInput.focus();
        }
    }

    // 2. Дополнительное подтверждение при удалении (на странице объекта)
    const deleteLink = document.querySelector('a.deletelink');
    if (deleteLink) {
        deleteLink.addEventListener('click', function (e) {
            if (!confirm('⚠️ Вы уверены, что хотите удалить этот объект?\nЭто действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    }

    // 3. Кнопка "Наверх" для длинных форм (появляется при прокрутке)
    if (document.body.classList.contains('change-form')) {
        const topButton = document.createElement('button');
        topButton.innerText = '↑';
        topButton.title = 'Наверх';
        topButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            background: #0d6efd;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            z-index: 1000;
            font-weight: bold;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s;
        `;

        topButton.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        document.body.appendChild(topButton);

        window.addEventListener('scroll', () => {
            topButton.style.opacity = window.scrollY > 300 ? '1' : '0';
        });
    }

    // 4. Подсказки для иконок в боковом меню (опционально)
    const sidebarLinks = document.querySelectorAll('.sidebar-menu a');
    sidebarLinks.forEach(link => {
        if (link.querySelector('.fa-newspaper')) link.title = 'Новости';
        if (link.querySelector('.fa-building')) link.title = 'Наши работы';
        if (link.querySelector('.fa-hard-hat')) link.title = 'Сотрудники';
        if (link.querySelector('.fa-envelope')) link.title = 'Заявки';
        if (link.querySelector('.fa-comments')) link.title = 'Сообщения чата';
    });

    // 5. Лог в консоль — для отладки подключения
    console.log('✅ admin-custom.js загружен. Админка улучшена!');
});