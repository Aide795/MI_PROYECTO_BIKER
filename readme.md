# API Biker Tapizados 🚀

Esta API permite gestionar solicitudes del formulario de cancelación de servicios.

## Endpoints:
- **GET /** → Verifica si la API está activa.
- **POST /cancelar_servicio** → Cancela un servicio enviando JSON.

### Ejemplo JSON para pruebas:
```json
{
  "servicio": "Tapizado Personalizado",
  "motivo": "Cliente no confirma pedido"
}
