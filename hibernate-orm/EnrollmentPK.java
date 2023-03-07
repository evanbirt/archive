/*
 * CS3810 - Principles of Database Systems - Spring 2021
 * Instructor: Thyago Mota
 * Description: DB 03 - EnrollmentPK
 * Student(s) Name(s): Evan Birt & Nicole Weickert & Naji Shamus
 */

import javax.persistence.Embeddable;
import java.io.Serializable;

@Embeddable
public class EnrollmentPK implements Serializable {

    private String code;
    private int id;

    public EnrollmentPK(String code, int id) {
        this.code = code;
        this.id = id;
    }

    public EnrollmentPK() {
    }

    public String getCode(String code) {
        return this.code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public int getId(int id) {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }
}