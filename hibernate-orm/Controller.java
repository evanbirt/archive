/*
 * CS3810 - Principles of Database Systems - Spring 2021
 * Instructor: Thyago Mota
 * Description: DB 03 - EnrollmentPK
 * Student(s) Name(s): Evan Birt & Nicole Weickert & Naji Shamus
 */

import org.hibernate.Session;
import org.hibernate.internal.SessionImpl;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.Query;
import java.sql.Connection;
import java.util.List;

public class Controller {

    private EntityManager em;
    private Session session;
    private Object EnrollmentPK;

    public Controller() {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("db03");
        em = emf.createEntityManager();
        session = em.unwrap(Session.class);
    }

    // TODO: return a Student entity from the given id (or null if the entity does not exist)
    public Student getStudent(int id) {
        return session.find(Student.class, id);
    }

    // TODO: add the given student entity, returning true/false depending whether the operation was successful or not
    public boolean addStudent(final Student student) {
        try {
            session.getTransaction().begin();
            session.persist(student);
            session.getTransaction().commit();
            session.close();
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    // TODO: return a list of all Course entities
    public List<Course> getCourses() {
        String hql = "FROM Course";
        Query query = session.createQuery(hql);
        List results = query.getResultList();
        return results;
    }

    // TODO: enroll a student to a course based on the given parameters, returning true/false depending whether the operation was successful or not
    public boolean enrollStudent(String code, int id) {
        try {
            em.getTransaction().begin();
            Enrollment enr = new Enrollment();
            EnrollmentPK epk = new EnrollmentPK();
            epk.setCode(code);
            epk.setId(id);
            enr.setEnrollmentPK(epk);
            em.persist(enr);
            em.getTransaction().commit();
            return true;
        } catch(Exception e) {
            return false;
        }
    }

    // TODO: drop a student from a course based on the given parameters, returning true/false depending whether the operation was successful or not
    public boolean dropStudent(String code, int id) {
        try {
            em.getTransaction().begin();
            EnrollmentPK epk = new EnrollmentPK();
            epk.setCode(code);
            epk.setId(id);
            Enrollment enr = em.find(Enrollment.class, epk);
            em.remove(enr);
            em.getTransaction().commit();
        } catch(Exception e) {
            return false;
        }
        return true;
    }

    // TODO: return a list of all Student entities enrolled in the given course (hint: use the stored procedure 'list_students')
    public List<Student> getStudentsEnrolled(String course) {
        SessionImpl sessionImpl = (SessionImpl) session;
        Connection conn = sessionImpl.connection();
        return sessionImpl.createSQLQuery("CALL list_students(:code)").addEntity(Student.class).setParameter("code", course).list();
    }
}