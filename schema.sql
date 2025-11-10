DROP DATABASE `prototype_db`;
CREATE DATABASE `prototype_db`;
CREATE TABLE `service` (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    `service_name` ENUM(
        "Caja",
        "Area de Servicio",
        "Socios fallecidos/certificados de deposito",
        "Descuento Nominal",
        "Departamento de Cobros"
    ) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
CREATE TABLE branch (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_name ENUM(
        "Manatí Central",
        "Manati Plaza",
        "Mortgage and commercial center",
        "Vega Baja",
        "Barceloneta",
        "Ciales Centro",
        "Ciales Expreso"
    ) NOT NULL
);
CREATE TABLE offers (
    offers_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_id INT NOT NULL,
    service_id INT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES `service`(service_id) ON DELETE RESTRICT,
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE RESTRICT,
    UNIQUE KEY unique_branch_service (branch_id, service_id)
);
CREATE TABLE employee (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(1),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `role` ENUM('employee', 'branch_admin', 'general_admin') NOT NULL,
    employee_status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE RESTRICT
);
CREATE TABLE password_reset (
    password_reset_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    password_reset_token VARCHAR(255) NOT NULL UNIQUE,
    token_secret VARCHAR(255) NOT NULL,
    token_expires DATETIME,
    new_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE RESTRICT
);
CREATE TABLE turn (
    turn_id INT PRIMARY KEY AUTO_INCREMENT,
    turn_number INT NOT NULL,
    `status` ENUM(
        'waiting',
        'called',
        'in_progress',
        'cancelled'
    ) NOT NULL DEFAULT 'waiting',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    employee_id INT NULL,
    called_at DATETIME NULL,
    completed_at DATETIME NULL,
    comment TEXT NULL,
    customer_name VARCHAR(50) NULL,
    purpose TEXT NULL,
    branch_id INT NOT NULL,
    service_id INT NOT NULL,
    new_turn_id INT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE RESTRICT,
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id) ON DELETE RESTRICT,
    FOREIGN KEY (service_id) REFERENCES `service`(service_id) ON DELETE RESTRICT,
    FOREIGN KEY (new_turn_id) REFERENCES turn(turn_id) ON DELETE RESTRICT
);
CREATE TABLE `modify` (
    modify_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT NOT NULL,
    edited_employee_id INT NOT NULL,
    `action` INT NOT NULL,
    modified_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES employee(employee_id) ON DELETE RESTRICT,
    FOREIGN KEY (edited_employee_id) REFERENCES employee(employee_id) ON DELETE RESTRICT
);
INSERT INTO branch (branch_name)
VALUES ("Manatí Central");
INSERT INTO employee (
        branch_id,
        first_name,
        middle_initial,
        last_name,
        email,
        password,
        role,
        employee_status,
        is_active
    )
VALUES (
        1,
        "John",
        "R",
        "Williams",
        "your-email@gmail.com",
        "$5$rounds=535000$D6BSFM/AgzQ39Aet$AWk9J/pOwBaslIHErUvy807x1sXopPaUhGyiZ6oRYT2",
        "branch_admin",
        "active",
        true
    );
INSERT INTO employee (
        branch_id,
        first_name,
        last_name,
        email,
        password,
        role,
        employee_status,
        is_active
    )
VALUES (
        1,
        "Pepo",
        "del Pueblo",
        "p.delpueblo@coopmanati.net",
        "$5$rounds=535000$Kmh7NxLSR8Vd4mYU$9VlYElT6Fv8hOq2VLU6rHDnuvnmQYyynwwpF7mB1T2A",
        "employee",
        "active",
        true
    );