package autonoma.torneoyugioh.models;

/**
 * Modelo que reprtesenta los datos de una persona
 *
 * @author DOSSA0110
 * @version 1.0.0
 * @since 2024/03/01
 */
public class Personaje {

    // Atributos
    /**
     * Nombre del personaje de la carta
     */
    private String nombre;
    /**
     * Cantidad de poder del personaje
     */
    private int poderAtaque;
    /**
     * Capacidad de defensa del personaje
     */
    private int capacidadDefensa;

    // Metodo Constructor
    public Personaje(String nombre, int poderAtaque, int capacidadDefensa) {
        this.nombre = nombre;
        this.poderAtaque = poderAtaque;
        this.capacidadDefensa = capacidadDefensa;
    }

    // Metodos de acceso
    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getPoderAtaque() {
        return poderAtaque;
    }

    public void setPoderAtaque(int poderAtaque) {
        this.poderAtaque = poderAtaque;
    }

    public int getCapacidadDefensa() {
        return capacidadDefensa;
    }

    public void setCapacidadDefensa(int capacidadDefensa) {
        this.capacidadDefensa = capacidadDefensa;
    }

}
