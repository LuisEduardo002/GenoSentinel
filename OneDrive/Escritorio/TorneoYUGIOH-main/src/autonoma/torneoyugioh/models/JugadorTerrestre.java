package autonoma.torneoyugioh.models;

/**
 * Modelo que representa los datos de Jugador Terrestre
 *
 * @author Dajumaks (Josue Castaño)
 * @version 1.0.0
 * @since 2024/03/06
 */


/**
 * extends Jugador: se refiere a los datos almacenados de otra Clase ----- int
 * numeroVictorias, int puntosExtra.
 */
public class JugadorTerrestre extends Jugador {

    ////////////////// 
    ////////////Atributos requeridos en el taller
    private String paisOrigen;
    private int edad;

    /**
     * extends Jugador: se refiere a los datos almacenados de otra Clase ----- int numeroVictorias, int puntosExtra.
     * Parametros necesarios:
     * @param nombre
     * @param numeroVictorias
     * @param puntosExtra
     * @param paisOrigen
     * @param edad
     */
    public JugadorTerrestre(String nombre, int numeroVictorias, int puntosExtra, String paisOrigen, int edad) {
        /**
         * La clave super es usada para acceder y llamar funciones del padre de
         * un objeto.
         */
        super(nombre, numeroVictorias, puntosExtra);
        this.paisOrigen = paisOrigen;
        this.edad = edad;
    }
    /////////////
    //////Getters y setters

    public String getPaisOrigen() {
        return paisOrigen;
    }

    public void setPaisOrigen(String paisOrigen) {
        this.paisOrigen = paisOrigen;
    }

    public int getEdad() {
        return edad;
    }

    public void setEdad(int edad) {
        this.edad = edad;
    }
}
