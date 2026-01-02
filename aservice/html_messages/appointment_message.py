def get_appointment_html_message(date, time, services):
    html_message = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; text-align: justify;">
                        <h2>Здравствуйте!</h2>
                        <p style="font-size: 16px; color: #555555;">
                            Вы успешно записались в автосервис <strong>AutoMaster</strong>.
                        </p>
                        <p style="font-size: 16px; color: #555555;">
                            <p style="font-size: 16px; color: #555555;">
                                Дублируем информацию записи:
                            </p>
                            <strong>Дата:</strong> {date}<br>
                            <strong>Время:</strong> {time}<br>
                            <strong>Услуга:</strong> {services}
                        </p>
                        <p style="font-size: 14px; color: #999999; margin-top: 30px;">
                            Если вы не записывались, просто проигнорируйте это сообщение.
                        </p>
                    </body>
                </html>
                """
    return html_message
