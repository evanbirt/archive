/*
 * CS3810 - Principles of Database Systems - Spring 2021
 * Instructor: Thyago Mota
 * Description: DB 03 - EnrollmentPK
 * Student(s) Name(s): Evan Birt & Nicole Weickert & Naji Shamus
 */

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = "enrollments")
public class Enrollment implements Serializable {
    @EmbeddedId
    private EnrollmentPK enrollmentPK;

    @JoinColumns({
            @JoinColumn(name = "students", insertable = false, updatable = false),
            @JoinColumn(name = "courses", insertable = false, updatable = false)
    })

    public EnrollmentPK getEnrollmentPK(EnrollmentPK epk) {
        return enrollmentPK;
    }

    public void setEnrollmentPK(EnrollmentPK enrollmentPK) {
        this.enrollmentPK = enrollmentPK;
    }
}