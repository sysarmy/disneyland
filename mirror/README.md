# Mirror
Desde Octubre de 2019 a Enero de 2024 hosteamos mirror.eze.sysarmy.com, en el momento de su creacion la disponibilidad de mirrors locales era limitada muchos main mirrors de argentina eran de Brasil. 
<img src="https://raw.githubusercontent.com/sysarmy/disneyland/master/mirror/final_shot.png">

FAQ
-
- Por qué dieron de baja el mirror?
Aunque no parece mantener un mirror lleva tiempo, esfuerzo y recursos. El setup que teníamos armado gracias a la colaboración de los sponsors funcionó bien por un tiempo pero no nos permitía escalar. Paralelamente aparecieron otros mirrors en argentina por lo que no debería haber mucha disrupción para los usuarios. Fue preferible desafectar el mirror antes que el riesgo de generar problemas a los usuarios finales.
- Buscaron otros sponsors? 
Si, pero sin resultados positivos.
- Qué necesitan para que vuelva a la vida? Requerimientos básicos:
     - 1 Gbps simétrico de internet.
     - un /29 o al menos 2 ip's publicas detras de un NAT.
     - IPv6
     - Con housing: 1U de rack. Nosotros ponemos el server.
     - Sin housing: 1 vm con 8vcpu, 32G of ram y 20Tb de storage.

Facts falopa:
-
- Teníamos mucho trafico de uruguay porque nuestro mirror al tener peering directo con Antel les daba mejor ping.
- Los bots son una 💩
- Tratar de servir iso's desde la cache de varnish, LOL en que estabamos pensando.
- IO mata CPU/RAM.
- Hay mas IPV6 del que parece.
- XFS te puede dejar a gamba en un corte de luz.
- Los mirror admins son mas lentos que atlassian para responder emails.
- Toda la distribucion del opensource esta atada con bash y rsync.

Datadog
-
Screenshot finales de nuestro austero monitoreo de tráfico.
<img src="https://raw.githubusercontent.com/sysarmy/disneyland/master/mirror/datadog_1.png">
<img src="https://raw.githubusercontent.com/sysarmy/disneyland/master/mirror/datadog_2.png">
