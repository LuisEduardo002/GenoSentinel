package autonoma.torneoyugioh.models;
/**
 *
 * @author Samuel Esteban Herrera Bedoya
 * @since 2024-03-7
 */
public class Jugador 
{
    private String nombre;
    private int numeroVictorias;
    private int puntosExtra;

    public Jugador(String nombre, int puntosExtra, int numeroVictorias) {
        this.nombre = nombre;
        this.puntosExtra = puntosExtra;
        this.numeroVictorias = numeroVictorias;
    }
    
    
}
