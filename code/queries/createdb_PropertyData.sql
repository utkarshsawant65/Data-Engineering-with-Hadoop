-- Create the database
CREATE DATABASE PropertyData;

-- Use the created database
USE PropertyData;

-- Create the Place table
CREATE TABLE Place (
    PlaceID INT PRIMARY KEY,
    PlaceName VARCHAR(255)
);

-- Create the PropertyType table
CREATE TABLE PropertyType (
    PropertyTypeID INT PRIMARY KEY,
    TypeName VARCHAR(255)
);

-- Create the Property table
CREATE TABLE Property (
    SerialNumber INT PRIMARY KEY,
    ListYear INT,
    Place VARCHAR(255),
    PlaceID INT,
    Address VARCHAR(255),
    AssessedValue INT,
    SaleAmount INT,
    SalesRatio FLOAT,
    PropertyType VARCHAR(255),
    PropertyTypeID INT,
    ResidentialType VARCHAR(255),
    FOREIGN KEY (PlaceID) REFERENCES Place(PlaceID),
    FOREIGN KEY (PropertyTypeID) REFERENCES PropertyType(PropertyTypeID)
);

-- Create the RetailStore table
CREATE TABLE RetailStore (
    LicenseNumber INT PRIMARY KEY,
    Place VARCHAR(255),
    PlaceID INT,
    Address VARCHAR(255),
    OperationType VARCHAR(255),
    StoreName VARCHAR(255),
    EntityName VARCHAR(255),
    DBAName VARCHAR(255),
    FOREIGN KEY (PlaceID) REFERENCES Place(PlaceID)
);

-- Create the CrimeData table
CREATE TABLE CrimeData (
    ID INT PRIMARY KEY,
    CaseNumber VARCHAR(50),
    Place VARCHAR(255),
    PlaceID INT,
    Block VARCHAR(255),
    IUCR INT,
    PrimaryType VARCHAR(255),
    Description VARCHAR(255),
    LocationDescription VARCHAR(255),
    Arrest VARCHAR(255),
    Domestic VARCHAR(255),
    FOREIGN KEY (PlaceID) REFERENCES Place(PlaceID)
);

-- Create the Pharmacy table
CREATE TABLE Pharmacy (
    credentialid INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    fullcredentialcode VARCHAR(50),
    PlaceID INT,
    PlaceName VARCHAR(255)
);
