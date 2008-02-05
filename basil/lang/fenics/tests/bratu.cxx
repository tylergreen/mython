// This example will solve the Bratu problem eventually
static char help[] = "This example solves the Bratu problem.\n\n";

#define ALE_HAVE_CXX_ABI

#include <petscmesh.hh>
#include <petscmesh_viewers.hh>
#include <petscmesh_formats.hh>
#include <petscdmmg.h>
#include "Generator.hh"

#include FENICS_HEADER

using ALE::Obj;
typedef enum {RUN_FULL, RUN_TEST, RUN_MESH} RunType;
typedef enum {NEUMANN, DIRICHLET} BCType;
typedef enum {ASSEMBLY_FULL, ASSEMBLY_STORED, ASSEMBLY_CALCULATED} AssemblyType;
typedef union {SectionReal section; Vec vec;} ExactSolType;

typedef struct {
  PetscInt      debug;                       // The debugging level
  RunType       run;                         // The run type
  PetscInt      dim;                         // The topological mesh dimension
  PetscTruth    reentrantMesh;               // Generate a reentrant mesh?
  PetscTruth    circularMesh;                // Generate a circular mesh?
  PetscTruth    refineSingularity;           // Generate an a priori graded mesh for the poisson problem
  PetscTruth    generateMesh;                // Generate the unstructure mesh
  PetscTruth    interpolate;                 // Generate intermediate mesh elements
  PetscReal     refinementLimit;             // The largest allowable cell volume
  char          baseFilename[2048];          // The base filename for mesh files
  PetscScalar (*func)(const double []);      // The function to project
  BCType        bcType;                      // The type of boundary conditions
  PetscScalar (*exactFunc)(const double []); // The exact solution function
  ExactSolType  exactSol;                    // The discrete exact solution
  ExactSolType  error;                       // The discrete cell-wise error
  AssemblyType  operatorAssembly;            // The type of operator assembly 
  double (*integrate)(const double *, const double *, const int, double (*)(const double *)); // Basis functional application
  double        lambda;                      // The parameter controlling nonlinearity
  double        reentrant_angle;              // The angle for the reentrant corner.
} Options;

#include "bratu_quadrature.h"

PetscScalar lambda = 0.0;

PetscScalar zero(const double x[]) {
  return 0.0;
}

PetscScalar constant(const double x[]) {
  return -4.0;
}

PetscScalar nonlinear_2d(const double x[]) {
  return -4.0 - lambda*PetscExpScalar(x[0]*x[0] + x[1]*x[1]);
}

PetscScalar singularity_2d(const double x[]) {
  return 0.;
}

PetscScalar singularity_exact_2d(const double x[]) {
  double r = sqrt(x[0]*x[0] + x[1]*x[1]);
  double theta;
  if (r == 0.) {
    return 0.;
  } else theta = asin(x[1]/r);
  if (x[0] < 0) {
    theta = 2*M_PI - theta;
  }
  return pow(r, 2./3.)*sin((2./3.)*theta);
}

PetscScalar singularity_exact_3d(const double x[]) {
  return sin(x[0] + x[1] + x[2]);  
}

PetscScalar singularity_3d(const double x[]) {
  return (3)*sin(x[0] + x[1] + x[2]);
}

PetscScalar linear_2d(const double x[]) {
  return -6.0*(x[0] - 0.5) - 6.0*(x[1] - 0.5);
}

PetscScalar quadratic_2d(const double x[]) {
  return x[0]*x[0] + x[1]*x[1];
}

PetscScalar cubic_2d(const double x[]) {
  return x[0]*x[0]*x[0] - 1.5*x[0]*x[0] + x[1]*x[1]*x[1] - 1.5*x[1]*x[1] + 0.5;
}

PetscScalar nonlinear_3d(const double x[]) {
  return -4.0 - lambda*PetscExpScalar((2.0/3.0)*(x[0]*x[0] + x[1]*x[1] + x[2]*x[2]));
}

PetscScalar linear_3d(const double x[]) {
  return -6.0*(x[0] - 0.5) - 6.0*(x[1] - 0.5) - 6.0*(x[2] - 0.5);
}

PetscScalar quadratic_3d(const double x[]) {
  return (2.0/3.0)*(x[0]*x[0] + x[1]*x[1] + x[2]*x[2]);
}

PetscScalar cubic_3d(const double x[]) {
  return x[0]*x[0]*x[0] - 1.5*x[0]*x[0] + x[1]*x[1]*x[1] - 1.5*x[1]*x[1] + x[2]*x[2]*x[2] - 1.5*x[2]*x[2] + 0.75;
}

PetscScalar cos_x(const double x[]) {
  return cos(2.0*PETSC_PI*x[0]);
}

#undef __FUNCT__
#define __FUNCT__ "ProcessOptions"
PetscErrorCode ProcessOptions(MPI_Comm comm, Options *options)
{
  const char    *runTypes[3] = {"full", "test", "mesh"};
  const char    *bcTypes[2]  = {"neumann", "dirichlet"};
  const char    *asTypes[4]  = {"full", "stored", "calculated"};
  ostringstream  filename;
  PetscInt       run, bc, as;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  options->debug            = 0;
  options->run              = RUN_FULL;
  options->dim              = 2;
  options->generateMesh     = PETSC_TRUE;
  options->interpolate      = PETSC_TRUE;
  options->refinementLimit  = 0.0;
  options->bcType           = DIRICHLET;
  options->operatorAssembly = ASSEMBLY_FULL;
  options->lambda           = 0.0;
  options->reentrantMesh    = PETSC_FALSE;
  options->circularMesh    = PETSC_FALSE;
  options->refineSingularity= PETSC_FALSE;

  ierr = PetscOptionsBegin(comm, "", "Bratu Problem Options", "DMMG");CHKERRQ(ierr);
    ierr = PetscOptionsInt("-debug", "The debugging level", "bratu.cxx", options->debug, &options->debug, PETSC_NULL);CHKERRQ(ierr);
    run = options->run;
    ierr = PetscOptionsEList("-run", "The run type", "bratu.cxx", runTypes, 3, runTypes[options->run], &run, PETSC_NULL);CHKERRQ(ierr);
    options->run = (RunType) run;
    ierr = PetscOptionsInt("-dim", "The topological mesh dimension", "bratu.cxx", options->dim, &options->dim, PETSC_NULL);CHKERRQ(ierr);
    ierr = PetscOptionsTruth("-reentrant", "Make a reentrant-corner mesh", "bratu.cxx", options->reentrantMesh, &options->reentrantMesh, PETSC_NULL);CHKERRQ(ierr);
    ierr = PetscOptionsTruth("-circular_mesh", "Make a reentrant-corner mesh", "bratu.cxx", options->circularMesh, &options->circularMesh, PETSC_NULL);CHKERRQ(ierr);
    ierr = PetscOptionsTruth("-singularity", "Refine the mesh around a singularity with a priori poisson error estimation", "bratu.cxx", options->refineSingularity, &options->refineSingularity, PETSC_NULL);CHKERRQ(ierr);
    ierr = PetscOptionsTruth("-generate", "Generate the unstructured mesh", "bratu.cxx", options->generateMesh, &options->generateMesh, PETSC_NULL);CHKERRQ(ierr);
    ierr = PetscOptionsTruth("-interpolate", "Generate intermediate mesh elements", "bratu.cxx", options->interpolate, &options->interpolate, PETSC_NULL);CHKERRQ(ierr);
    ierr = PetscOptionsReal("-refinement_limit", "The largest allowable cell volume", "bratu.cxx", options->refinementLimit, &options->refinementLimit, PETSC_NULL);CHKERRQ(ierr);
    filename << "data/bratu_" << options->dim <<"d";
    ierr = PetscStrcpy(options->baseFilename, filename.str().c_str());CHKERRQ(ierr);
    ierr = PetscOptionsString("-base_filename", "The base filename for mesh files", "bratu.cxx", options->baseFilename, options->baseFilename, 2048, PETSC_NULL);CHKERRQ(ierr);
    bc = options->bcType;
    ierr = PetscOptionsEList("-bc_type","Type of boundary condition","bratu.cxx",bcTypes,2,bcTypes[options->bcType],&bc,PETSC_NULL);CHKERRQ(ierr);
    options->bcType = (BCType) bc;
    as = options->operatorAssembly;
    ierr = PetscOptionsEList("-assembly_type","Type of operator assembly","bratu.cxx",asTypes,3,asTypes[options->operatorAssembly],&as,PETSC_NULL);CHKERRQ(ierr);
    options->operatorAssembly = (AssemblyType) as;
    ierr = PetscOptionsReal("-lambda", "The parameter controlling nonlinearity", "bratu.cxx", options->lambda, &options->lambda, PETSC_NULL);CHKERRQ(ierr);
    lambda = options->lambda;
  ierr = PetscOptionsEnd();

  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "CreatePartition"
// Creates a field whose value is the processor rank on each element
PetscErrorCode CreatePartition(Mesh mesh, SectionInt *partition)
{
  Obj<ALE::Mesh> m;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = MeshGetCellSectionInt(mesh, 1, partition);CHKERRQ(ierr);
  const Obj<ALE::Mesh::label_sequence>&     cells = m->heightStratum(0);
  const ALE::Mesh::label_sequence::iterator end   = cells->end();
  const int                                 rank  = m->commRank();

  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != end; ++c_iter) {
    ierr = SectionIntUpdate(*partition, *c_iter, &rank);
  }
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "ViewSection"
PetscErrorCode ViewSection(Mesh mesh, SectionReal section, const char filename[], bool vertexwise = true)
{
  MPI_Comm       comm;
  SectionInt     partition;
  PetscViewer    viewer;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscObjectGetComm((PetscObject) mesh, &comm);CHKERRQ(ierr);
  ierr = PetscViewerCreate(comm, &viewer);CHKERRQ(ierr);
  ierr = PetscViewerSetType(viewer, PETSC_VIEWER_ASCII);CHKERRQ(ierr);
  ierr = PetscViewerSetFormat(viewer, PETSC_VIEWER_ASCII_VTK);CHKERRQ(ierr);
  ierr = PetscViewerFileSetName(viewer, filename);CHKERRQ(ierr);
  ierr = MeshView(mesh, viewer);CHKERRQ(ierr);
  if (!vertexwise) {ierr = PetscViewerSetFormat(viewer, PETSC_VIEWER_ASCII_VTK_CELL);CHKERRQ(ierr);}
  ierr = SectionRealView(section, viewer);CHKERRQ(ierr);
  ierr = CreatePartition(mesh, &partition);CHKERRQ(ierr);
  ierr = PetscViewerPushFormat(viewer, PETSC_VIEWER_ASCII_VTK_CELL);CHKERRQ(ierr);
  ierr = SectionIntView(partition, viewer);CHKERRQ(ierr);
  ierr = SectionIntDestroy(partition);CHKERRQ(ierr);
  ierr = PetscViewerPopFormat(viewer);CHKERRQ(ierr);
  ierr = PetscViewerDestroy(viewer);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "ViewMesh"
PetscErrorCode ViewMesh(Mesh mesh, const char filename[])
{
  MPI_Comm       comm;
  SectionInt     partition;
  PetscViewer    viewer;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscObjectGetComm((PetscObject) mesh, &comm);CHKERRQ(ierr);
  ierr = PetscViewerCreate(comm, &viewer);CHKERRQ(ierr);
  ierr = PetscViewerSetType(viewer, PETSC_VIEWER_ASCII);CHKERRQ(ierr);
  ierr = PetscViewerSetFormat(viewer, PETSC_VIEWER_ASCII_VTK);CHKERRQ(ierr);
  ierr = PetscViewerFileSetName(viewer, filename);CHKERRQ(ierr);
  ierr = MeshView(mesh, viewer);CHKERRQ(ierr);
  ierr = CreatePartition(mesh, &partition);CHKERRQ(ierr);
  ierr = PetscViewerPushFormat(viewer, PETSC_VIEWER_ASCII_VTK_CELL);CHKERRQ(ierr);
  ierr = SectionIntView(partition, viewer);CHKERRQ(ierr);
  ierr = PetscViewerPopFormat(viewer);CHKERRQ(ierr);
  ierr = SectionIntDestroy(partition);CHKERRQ(ierr);
  ierr = PetscViewerDestroy(viewer);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#undef __FUNCT__  
#define __FUNCT__ "MeshRefineSingularity"
PetscErrorCode PETSCDM_DLLEXPORT MeshRefineSingularity(Mesh mesh, MPI_Comm comm, double * singularity, double factor, Mesh *refinedMesh)
{
  ALE::Obj<ALE::Mesh> oldMesh;
  double              oldLimit;
  PetscErrorCode      ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, oldMesh);CHKERRQ(ierr);
  ierr = MeshCreate(comm, refinedMesh);CHKERRQ(ierr);
  int dim = oldMesh->getDimension();
  oldLimit = oldMesh->getMaxVolume();
  //double oldLimInv = 1./oldLimit;
  double curLimit, tmpLimit;
  double minLimit = oldLimit/16384.;             //arbitrary;
  const ALE::Obj<ALE::Mesh::real_section_type>& coordinates = oldMesh->getRealSection("coordinates");
  const ALE::Obj<ALE::Mesh::real_section_type>& volume_limits = oldMesh->getRealSection("volume_limits");
  volume_limits->setFiberDimension(oldMesh->heightStratum(0), 1);
  oldMesh->allocate(volume_limits);
  const ALE::Obj<ALE::Mesh::label_sequence>& cells = oldMesh->heightStratum(0);
  ALE::Mesh::label_sequence::iterator c_iter = cells->begin();
  ALE::Mesh::label_sequence::iterator c_iter_end = cells->end();
  double centerCoords[dim];
  while (c_iter != c_iter_end) {
    const double * coords = oldMesh->restrict(coordinates, *c_iter);
    for (int i = 0; i < dim; i++) {
      centerCoords[i] = 0;
      for (int j = 0; j < dim+1; j++) {
        centerCoords[i] += coords[j*dim+i];
      }
      centerCoords[i] = centerCoords[i]/(dim+1);
    }
    double dist = 0.;
    for (int i = 0; i < dim; i++) {
      dist += (centerCoords[i] - singularity[i])*(centerCoords[i] - singularity[i]);
    }
    if (dist > 0.) {
      dist = sqrt(dist);
      double mu = pow(dist, factor);
      //PetscPrintf(oldMesh->comm(), "%f\n", mu);
      tmpLimit = oldLimit*pow(mu, dim);
      if (tmpLimit > minLimit) {
        curLimit = tmpLimit;
      } else curLimit = minLimit;
    } else curLimit = minLimit;
    //PetscPrintf(oldMesh->comm(), "%f, %f\n", dist, tmpLimit);
    volume_limits->updatePoint(*c_iter, &curLimit);
    c_iter++;
  }
  ALE::Obj<ALE::Mesh> newMesh = ALE::Generator::refineMesh(oldMesh, volume_limits, true);
  ierr = MeshSetMesh(*refinedMesh, newMesh);CHKERRQ(ierr);
  const ALE::Obj<ALE::Mesh::real_section_type>& s = newMesh->getRealSection("default");
  const Obj<std::set<std::string> >& discs = oldMesh->getDiscretizations();

  for(std::set<std::string>::const_iterator f_iter = discs->begin(); f_iter != discs->end(); ++f_iter) {
    newMesh->setDiscretization(*f_iter, oldMesh->getDiscretization(*f_iter));
  }
  newMesh->setupField(s);
  PetscFunctionReturn(0);
}

#undef __FUNCT__  
#define __FUNCT__ "MeshRefineSingularity_Fichera"
PetscErrorCode PETSCDM_DLLEXPORT MeshRefineSingularity_Fichera(Mesh mesh, MPI_Comm comm, double * singularity, double factor, Mesh *refinedMesh)
{
  ALE::Obj<ALE::Mesh> oldMesh;
  double              oldLimit;
  PetscErrorCode      ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, oldMesh);CHKERRQ(ierr);
  ierr = MeshCreate(comm, refinedMesh);CHKERRQ(ierr);
  int dim = oldMesh->getDimension();
  oldLimit = oldMesh->getMaxVolume();
  //double oldLimInv = 1./oldLimit;
  double curLimit, tmpLimit;
  double minLimit = oldLimit/16384.;             //arbitrary;
  const ALE::Obj<ALE::Mesh::real_section_type>& coordinates = oldMesh->getRealSection("coordinates");
  const ALE::Obj<ALE::Mesh::real_section_type>& volume_limits = oldMesh->getRealSection("volume_limits");
  volume_limits->setFiberDimension(oldMesh->heightStratum(0), 1);
  oldMesh->allocate(volume_limits);
  const ALE::Obj<ALE::Mesh::label_sequence>& cells = oldMesh->heightStratum(0);
  ALE::Mesh::label_sequence::iterator c_iter = cells->begin();
  ALE::Mesh::label_sequence::iterator c_iter_end = cells->end();
  double centerCoords[dim];
  while (c_iter != c_iter_end) {
    const double * coords = oldMesh->restrict(coordinates, *c_iter);
    for (int i = 0; i < dim; i++) {
      centerCoords[i] = 0;
      for (int j = 0; j < dim+1; j++) {
        centerCoords[i] += coords[j*dim+i];
      }
      centerCoords[i] = centerCoords[i]/(dim+1);
      //PetscPrintf(oldMesh->comm(), "%f, ", centerCoords[i]);
    }
    //PetscPrintf(oldMesh->comm(), "\n");
    double dist = 0.;
    double cornerdist = 0.;
    //HERE'S THE DIFFERENCE: if centercoords is less than the singularity coordinate for each direction, include that direction in the distance
    /*
    for (int i = 0; i < dim; i++) {
      if (centerCoords[i] <= singularity[i]) {
        dist += (centerCoords[i] - singularity[i])*(centerCoords[i] - singularity[i]);
      }
    }
    */
    //determine: the per-dimension distance: cases
    for (int i = 0; i < dim; i++) {
      cornerdist = 0.;
      if (centerCoords[i] > singularity[i]) {
        for (int j = 0; j < dim; j++) {
          if (j != i) cornerdist += (centerCoords[j] - singularity[j])*(centerCoords[j] - singularity[j]);
        }
        if (cornerdist < dist || dist == 0.) dist = cornerdist; 
      }
    }
    //patch up AROUND the corner by minimizing between the distance from the relevant axis and the singular vertex
    double singdist = 0.;
    for (int i = 0; i < dim; i++) {
      singdist += (centerCoords[i] - singularity[i])*(centerCoords[i] - singularity[i]);
    }
    if (singdist < dist || dist == 0.) dist = singdist;
    if (dist > 0.) {
      dist = sqrt(dist);
      double mu = pow(dist, factor);
      //PetscPrintf(oldMesh->comm(), "%f, %f\n", mu, dist);
      tmpLimit = oldLimit*pow(mu, dim);
      if (tmpLimit > minLimit) {
        curLimit = tmpLimit;
      } else curLimit = minLimit;
    } else curLimit = minLimit;
    //PetscPrintf(oldMesh->comm(), "%f, %f\n", dist, tmpLimit);
    volume_limits->updatePoint(*c_iter, &curLimit);
    c_iter++;
  }
  ALE::Obj<ALE::Mesh> newMesh = ALE::Generator::refineMesh(oldMesh, volume_limits, true);
  ierr = MeshSetMesh(*refinedMesh, newMesh);CHKERRQ(ierr);
  const ALE::Obj<ALE::Mesh::real_section_type>& s = newMesh->getRealSection("default");
  const Obj<std::set<std::string> >& discs = oldMesh->getDiscretizations();

  for(std::set<std::string>::const_iterator f_iter = discs->begin(); f_iter != discs->end(); ++f_iter) {
    newMesh->setDiscretization(*f_iter, oldMesh->getDiscretization(*f_iter));
  }
  newMesh->setupField(s);
  //  PetscPrintf(newMesh->comm(), "refined\n");
  PetscFunctionReturn(0);
}

EXTERN PetscErrorCode MeshIDBoundary(Mesh mesh);

#undef __FUNCT__
#define __FUNCT__ "CreateMesh"
PetscErrorCode CreateMesh(MPI_Comm comm, DM *dm, Options *options)
{
  Mesh           mesh;
  PetscTruth     view;
  PetscMPIInt    size;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  if (options->generateMesh) {
    Mesh boundary;

    ierr = MeshCreate(comm, &boundary);CHKERRQ(ierr);
    if (options->dim == 2) {
      double lower[2]  = {0.0, 0.0};
      double upper[2]  = {1.0, 1.0};
      double offset[2] = {0.5, 0.5};
      int    edges[2]  = {2, 2};
      Obj<ALE::Mesh> mB;

      if (options->circularMesh) {
        double arclen = 1.;
        if (options->reentrantMesh) {
          arclen = .9;
          options->reentrant_angle = .9;
        }
        mB = ALE::MeshBuilder::createCircularReentrantBoundary(comm, 100, 1., arclen, options->debug);
      } else if (options->reentrantMesh) {
        double reentrantlower[2] = {-1., -1.};
        options->reentrant_angle = .75;
        mB = ALE::MeshBuilder::createReentrantBoundary(comm, reentrantlower, upper, offset, options->debug);
      } else {
        mB = ALE::MeshBuilder::createSquareBoundary(comm, lower, upper, edges, options->debug);
      }
      ierr = MeshSetMesh(boundary, mB);CHKERRQ(ierr);
    } else if (options->dim == 3) {
      Obj<ALE::Mesh> mB;
      if (options->reentrantMesh) {
        double lower[3] = {-1., -1., -1.};
        double upper[3] = {1., 1., 1.};
        double offset[3] = {0.5, 0.5, 0.5};
        mB = ALE::MeshBuilder::createFicheraCornerBoundary(comm, lower, upper, offset, options->debug);
          
      } else {
        double lower[3] = {0.0, 0.0, 0.0};
        double upper[3] = {1.0, 1.0, 1.0};
        int    faces[3] = {3, 3, 3};

        mB = ALE::MeshBuilder::createCubeBoundary(comm, lower, upper, faces, options->debug);
      }
      ierr = MeshSetMesh(boundary, mB);CHKERRQ(ierr);
    } else {
      SETERRQ1(PETSC_ERR_SUP, "Dimension not supported: %d", options->dim);
    }
    ierr = MeshGenerate(boundary, options->interpolate, &mesh);CHKERRQ(ierr);
    ierr = MeshDestroy(boundary);CHKERRQ(ierr);
  } else {
    SETERRQ(PETSC_ERR_SUP, "No mesh formats supported");
  }
  ierr = MPI_Comm_size(comm, &size);CHKERRQ(ierr);
  if (size > 1) {
    Mesh parallelMesh;

    ierr = MeshDistribute(mesh, PETSC_NULL, &parallelMesh);CHKERRQ(ierr);
    ierr = MeshDestroy(mesh);CHKERRQ(ierr);
    mesh = parallelMesh;
  }
  if (options->refinementLimit > 0.0) {
    Mesh refinedMesh, refinedMesh2;

    ierr = MeshRefine(mesh, options->refinementLimit, options->interpolate, &refinedMesh);CHKERRQ(ierr);
    ierr = MeshDestroy(mesh);CHKERRQ(ierr);
    mesh = refinedMesh;
    if (options->refineSingularity) {
      double singularity[3] = {0.0, 0.0, 0.0};
      if (options->dim == 2) {
        ierr = MeshRefineSingularity(mesh, comm, singularity, options->reentrant_angle, &refinedMesh2);CHKERRQ(ierr);
      } else if (options->dim == 3) {
        ierr = MeshRefineSingularity_Fichera(mesh, comm, singularity, 0.75, &refinedMesh2);CHKERRQ(ierr);
      }
      ierr = MeshDestroy(mesh);CHKERRQ(ierr);
      mesh = refinedMesh2;
      ierr = MeshIDBoundary(mesh);CHKERRQ(ierr);
    }
  }
  if (options->bcType == DIRICHLET) {
    Obj<ALE::Mesh> m;

    ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
    m->markBoundaryCells("marker");
  }
  ierr = PetscOptionsHasName(PETSC_NULL, "-mesh_view_vtk", &view);CHKERRQ(ierr);
  if (view) {ierr = ViewMesh(mesh, "bratu.vtk");CHKERRQ(ierr);}
  ierr = PetscOptionsHasName(PETSC_NULL, "-mesh_view", &view);CHKERRQ(ierr);
  if (view) {
    Obj<ALE::Mesh> m;
    ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
    m->view("Mesh");
  }
  ierr = PetscOptionsHasName(PETSC_NULL, "-mesh_view_simple", &view);CHKERRQ(ierr);
  if (view) {ierr = MeshView(mesh, PETSC_VIEWER_STDOUT_WORLD);CHKERRQ(ierr);}
  *dm = (DM) mesh;
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "DestroyMesh"

PetscErrorCode DestroyMesh(DM dm, Options *options)
{
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshDestroy((Mesh) dm);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "DestroyExactSolution"
PetscErrorCode DestroyExactSolution(ExactSolType sol, Options *options)
{
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = SectionRealDestroy(sol.section);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "Function_Unstructured"
PetscErrorCode Function_Unstructured(Mesh mesh, SectionReal section, void *ctx)
{
  Options       *options = (Options *) ctx;
  PetscScalar  (*func)(const double *) = options->func;
  Obj<ALE::Mesh> m;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  const Obj<ALE::Mesh::real_section_type>& coordinates = m->getRealSection("coordinates");
  const Obj<ALE::Mesh::label_sequence>&    vertices    = m->depthStratum(0);

  for(ALE::Mesh::label_sequence::iterator v_iter = vertices->begin(); v_iter != vertices->end(); ++v_iter) {
    const ALE::Mesh::real_section_type::value_type *coords = coordinates->restrictPoint(*v_iter);
    const PetscScalar                               value  = (*func)(coords);

    ierr = SectionRealUpdate(section, *v_iter, &value);CHKERRQ(ierr);
  }
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "FormFunctions"
PetscErrorCode FormFunctions(DM dm, Options *options)
{
  Mesh           mesh = (Mesh) dm;
  SectionReal    F;
  Obj<ALE::Mesh> m;
  Obj<ALE::Mesh::real_section_type> s;
  PetscTruth     flag;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view_vtk", &flag);CHKERRQ(ierr);
  ierr = MeshGetSectionReal(mesh, "default", &F);CHKERRQ(ierr);
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = SectionRealGetSection(F, s);CHKERRQ(ierr);
  options->func = linear_2d;
  ierr = Function_Unstructured(mesh, F, (void *) options);CHKERRQ(ierr);
  if (flag) {ierr = ViewSection(mesh, F, "linear.vtk");CHKERRQ(ierr);}
  options->func = cos_x;
  ierr = Function_Unstructured(mesh, F, (void *) options);CHKERRQ(ierr);
  if (flag) {ierr = ViewSection(mesh, F, "cos.vtk");CHKERRQ(ierr);}
  ierr = SectionRealDestroy(F);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#if 0
#undef __FUNCT__
#define __FUNCT__ "Rhs_Unstructured"
PetscErrorCode Rhs_Unstructured(Mesh mesh, SectionReal X, SectionReal section, void *ctx)
{
  Options       *options = (Options *) ctx;
  PetscScalar  (*func)(const double *) = options->func;
  const double   lambda                = options->lambda;
  Obj<ALE::Mesh> m;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  const Obj<ALE::Discretization>&          disc          = m->getDiscretization("u");
  const int                                numQuadPoints = disc->getQuadratureSize();
  const double                            *quadPoints    = disc->getQuadraturePoints();
  const double                            *quadWeights   = disc->getQuadratureWeights();
  const int                                numBasisFuncs = disc->getBasisSize();
  const double                            *basis         = disc->getBasis();
  const double                            *basisDer      = disc->getBasisDerivatives();
  const Obj<ALE::Mesh::real_section_type>& coordinates   = m->getRealSection("coordinates");
  const Obj<ALE::Mesh::label_sequence>&    cells         = m->heightStratum(0);
  const int                                dim           = m->getDimension();
  double      *t_der, *b_der, *coords, *v0, *J, *invJ, detJ;
  PetscScalar *elemVec, *elemMat;

  ierr = SectionRealZero(section);CHKERRQ(ierr);
  ierr = PetscMalloc2(numBasisFuncs,PetscScalar,&elemVec,numBasisFuncs*numBasisFuncs,PetscScalar,&elemMat);CHKERRQ(ierr);
  ierr = PetscMalloc6(dim,double,&t_der,dim,double,&b_der,dim,double,&coords,dim,double,&v0,dim*dim,double,&J,dim*dim,double,&invJ);CHKERRQ(ierr);
  // Loop over cells
  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    ierr = PetscMemzero(elemVec, numBasisFuncs * sizeof(PetscScalar));CHKERRQ(ierr);
    ierr = PetscMemzero(elemMat, numBasisFuncs*numBasisFuncs * sizeof(PetscScalar));CHKERRQ(ierr);
    m->computeElementGeometry(coordinates, *c_iter, v0, J, invJ, detJ);
    if (detJ < 0) SETERRQ2(PETSC_ERR_ARG_OUTOFRANGE, "Invalid determinant %g for element %d", detJ, *c_iter);
    PetscScalar *x;

    ierr = SectionRealRestrict(X, *c_iter, &x);CHKERRQ(ierr);
    // Loop over quadrature points
    for(int q = 0; q < numQuadPoints; ++q) {
      for(int d = 0; d < dim; d++) {
        coords[d] = v0[d];
        for(int e = 0; e < dim; e++) {
          coords[d] += J[d*dim+e]*(quadPoints[q*dim+e] + 1.0);
        }
      }
      const PetscScalar funcVal  = (*func)(coords);
      PetscScalar       fieldVal = 0.0;

      for(int f = 0; f < numBasisFuncs; ++f) {
        fieldVal += x[f]*basis[q*numBasisFuncs+f];
      }
      // Loop over trial functions
      for(int f = 0; f < numBasisFuncs; ++f) {
        // Constant part
        elemVec[f] -= basis[q*numBasisFuncs+f]*funcVal*quadWeights[q]*detJ;
        // Linear part
        for(int d = 0; d < dim; ++d) {
          t_der[d] = 0.0;
          for(int e = 0; e < dim; ++e) t_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+f)*dim+e];
        }
        // Loop over basis functions
        for(int g = 0; g < numBasisFuncs; ++g) {
          // Linear part
          for(int d = 0; d < dim; ++d) {
            b_der[d] = 0.0;
            for(int e = 0; e < dim; ++e) b_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+g)*dim+e];
          }
          PetscScalar product = 0.0;
          for(int d = 0; d < dim; ++d) product += t_der[d]*b_der[d];
          elemMat[f*numBasisFuncs+g] += product*quadWeights[q]*detJ;
        }
        // Nonlinear part
        if (lambda != 0.0) {
          elemVec[f] -= basis[q*numBasisFuncs+f]*lambda*PetscExpScalar(fieldVal)*quadWeights[q]*detJ;
        }
      }
    }    
    // Add linear contribution
    for(int f = 0; f < numBasisFuncs; ++f) {
      for(int g = 0; g < numBasisFuncs; ++g) {
        elemVec[f] += elemMat[f*numBasisFuncs+g]*x[g];
      }
    }
    ierr = SectionRealUpdateAdd(section, *c_iter, elemVec);CHKERRQ(ierr);
  }
  ierr = PetscFree2(elemVec,elemMat);CHKERRQ(ierr);
  ierr = PetscFree6(t_der,b_der,coords,v0,J,invJ);CHKERRQ(ierr);
  // Exchange neighbors
  ierr = SectionRealComplete(section);CHKERRQ(ierr);
  // Subtract the constant
  if (m->hasRealSection("constant")) {
    const Obj<ALE::Mesh::real_section_type>& constant = m->getRealSection("constant");
    Obj<ALE::Mesh::real_section_type>        s;

    ierr = SectionRealGetSection(section, s);CHKERRQ(ierr);
    s->axpy(-1.0, constant);
  }
  PetscFunctionReturn(0);
}

#else

#undef __FUNCT__
#define __FUNCT__ "Rhs_Unstructured"
PetscErrorCode Rhs_Unstructured(Mesh mesh, SectionReal X, SectionReal section, void *ctx)
{
  Obj<ALE::Mesh> m;
  Obj<ALE::Mesh::real_section_type> x;
  Obj<ALE::Mesh::real_section_type> s;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = SectionRealGetSection(section, x);CHKERRQ(ierr);
  ierr = SectionRealGetSection(section, s);CHKERRQ(ierr);
  FENICS_Residual(m, x, s, ctx);
  PetscFunctionReturn(0);
}
#endif

#undef __FUNCT__
#define __FUNCT__ "CalculateError"
PetscErrorCode CalculateError(Mesh mesh, SectionReal X, double *error, void *ctx)
{
  Options       *options = (Options *) ctx;
  PetscScalar  (*func)(const double *) = options->exactFunc;
  Obj<ALE::Mesh> m;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  const Obj<ALE::Discretization>&          disc          = m->getDiscretization("u");
  const int                                numQuadPoints = disc->getQuadratureSize();
  const double                            *quadPoints    = disc->getQuadraturePoints();
  const double                            *quadWeights   = disc->getQuadratureWeights();
  const int                                numBasisFuncs = disc->getBasisSize();
  const double                            *basis         = disc->getBasis();
  const Obj<ALE::Mesh::real_section_type>& coordinates   = m->getRealSection("coordinates");
  const Obj<ALE::Mesh::label_sequence>&    cells         = m->heightStratum(0);
  const int                                dim           = m->getDimension();
  double *coords, *v0, *J, *invJ, detJ;
  double  localError = 0.0;

  ierr = PetscMalloc4(dim,double,&coords,dim,double,&v0,dim*dim,double,&J,dim*dim,double,&invJ);CHKERRQ(ierr);
  // Loop over cells
  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    PetscScalar *x;
    double       elemError = 0.0;

    m->computeElementGeometry(coordinates, *c_iter, v0, J, invJ, detJ);
    ierr = SectionRealRestrict(X, *c_iter, &x);CHKERRQ(ierr);
    // Loop over quadrature points
    for(int q = 0; q < numQuadPoints; ++q) {
      for(int d = 0; d < dim; d++) {
        coords[d] = v0[d];
        for(int e = 0; e < dim; e++) {
          coords[d] += J[d*dim+e]*(quadPoints[q*dim+e] + 1.0);
        }
      }
      const PetscScalar funcVal = (*func)(coords);

      double interpolant = 0.0;
      for(int f = 0; f < numBasisFuncs; ++f) {
        interpolant += x[f]*basis[q*numBasisFuncs+f];
      }
      elemError += (interpolant - funcVal)*(interpolant - funcVal)*quadWeights[q];
    }    
    if (options->debug) {
      std::cout << "Element " << *c_iter << " error: " << elemError << std::endl;
    }
    ierr = SectionRealUpdateAdd(options->error.section, *c_iter, &elemError);CHKERRQ(ierr);
    localError += elemError;
  }
  ierr = MPI_Allreduce(&localError, error, 1, MPI_DOUBLE, MPI_SUM, m->comm());CHKERRQ(ierr);
  ierr = PetscFree4(coords,v0,J,invJ);CHKERRQ(ierr);
  *error = sqrt(*error);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "FormWeakForms"
PetscErrorCode FormWeakForms(DM dm, Options *options)
{
  Mesh           mesh = (Mesh) dm;
  SectionReal    X, F;
  PetscTruth     flag;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view_vtk", &flag);CHKERRQ(ierr);
  ierr = MeshGetSectionReal(mesh, "default", &X);CHKERRQ(ierr);
  ierr = SectionRealZero(X);CHKERRQ(ierr);
  ierr = SectionRealDuplicate(X, &F);CHKERRQ(ierr);
  options->func = linear_2d;
  ierr = Rhs_Unstructured(mesh, X, F, (void *) options);CHKERRQ(ierr);
  if (flag) {ierr = ViewSection(mesh, F, "rhs_linear.vtk");CHKERRQ(ierr);}
  options->func = cos_x;
  ierr = Rhs_Unstructured(mesh, X, F, (void *) options);CHKERRQ(ierr);
  if (flag) {ierr = ViewSection(mesh, F, "rhs_cos.vtk");CHKERRQ(ierr);}
  ierr = SectionRealDestroy(F);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#if 0
EXTERN_C_BEGIN
#undef __FUNCT__
#define __FUNCT__ "Laplacian_2D_MF"
PetscErrorCode Laplacian_2D_MF(Mat A, Vec x, Vec y)
{
  Mesh             mesh;
  Obj<ALE::Mesh>   m;
  SectionReal      X, Y;
  PetscQuadrature *q;
  PetscErrorCode   ierr;

  PetscFunctionBegin;
  ierr = PetscObjectQuery((PetscObject) A, "mesh", (PetscObject *) &mesh);CHKERRQ(ierr);
  ierr = MatShellGetContext(A, (void **) &q);CHKERRQ(ierr);
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);

  ierr = MeshGetSectionReal(mesh, "work1", &X);CHKERRQ(ierr);
  ierr = MeshGetSectionReal(mesh, "work2", &Y);CHKERRQ(ierr);
  ierr = SectionRealToVec(X, mesh, SCATTER_REVERSE, x);CHKERRQ(ierr);

  const Obj<ALE::Mesh::real_section_type>& coordinates = m->getRealSection("coordinates");
  const Obj<ALE::Mesh::label_sequence>&    cells       = m->heightStratum(0);
  const int     numQuadPoints = q->numQuadPoints;
  const int     numBasisFuncs = q->numBasisFuncs;
  const double *quadWeights   = q->quadWeights;
  const double *basisDer      = q->basisDer;
  const int     dim           = m->getDimension();
  double       *t_der, *b_der, *v0, *J, *invJ, detJ;
  PetscScalar  *elemMat, *elemVec;

  ierr = PetscMalloc2(numBasisFuncs,PetscScalar,&elemVec,numBasisFuncs*numBasisFuncs,PetscScalar,&elemMat);CHKERRQ(ierr);
  ierr = PetscMalloc5(dim,double,&t_der,dim,double,&b_der,dim,double,&v0,dim*dim,double,&J,dim*dim,double,&invJ);CHKERRQ(ierr);
  // Loop over cells
  ierr = SectionRealZero(Y);CHKERRQ(ierr);
  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    ierr = PetscMemzero(elemMat, numBasisFuncs*numBasisFuncs * sizeof(PetscScalar));CHKERRQ(ierr);
    m->computeElementGeometry(coordinates, *c_iter, v0, J, invJ, detJ);
    // Loop over quadrature points
    for(int q = 0; q < numQuadPoints; ++q) {
      // Loop over trial functions
      for(int f = 0; f < numBasisFuncs; ++f) {
        for(int d = 0; d < dim; ++d) {
          t_der[d] = 0.0;
          for(int e = 0; e < dim; ++e) t_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+f)*dim+e];
        }
        // Loop over basis functions
        for(int g = 0; g < numBasisFuncs; ++g) {
          for(int d = 0; d < dim; ++d) {
            b_der[d] = 0.0;
            for(int e = 0; e < dim; ++e) b_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+g)*dim+e];
          }
          PetscScalar product = 0.0;
          for(int d = 0; d < dim; ++d) product += t_der[d]*b_der[d];
          elemMat[f*numBasisFuncs+g] += product*quadWeights[q]*detJ;
        }
      }
    }
    PetscScalar *ev;

    ierr = SectionRealRestrict(X, *c_iter, &ev);CHKERRQ(ierr);
    // Do local matvec
    for(int f = 0; f < numBasisFuncs; ++f) {
      elemVec[f] = 0.0;
      for(int g = 0; g < numBasisFuncs; ++g) {
        elemVec[f] += elemMat[f*numBasisFuncs+g]*ev[g];
      }
    }
    ierr = SectionRealUpdateAdd(Y, *c_iter, elemVec);CHKERRQ(ierr);
  }
  ierr = PetscFree2(elemVec,elemMat);CHKERRQ(ierr);
  ierr = PetscFree5(t_der,b_der,v0,J,invJ);CHKERRQ(ierr);
  ierr = SectionRealComplete(Y);CHKERRQ(ierr);

  ierr = SectionRealToVec(Y, mesh, SCATTER_FORWARD, y);CHKERRQ(ierr);
  ierr = SectionRealDestroy(X);CHKERRQ(ierr);
  ierr = SectionRealDestroy(Y);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}
EXTERN_C_END

#undef __FUNCT__
#define __FUNCT__ "Jac_Unstructured_Calculated"
PetscErrorCode Jac_Unstructured_Calculated(Mesh mesh, SectionReal section, Mat A, void *ctx)
{
  Obj<ALE::Mesh>   m;
  PetscQuadrature *q;
  PetscErrorCode   ierr;

  PetscFunctionBegin;
  ierr = MatShellSetOperation(A, MATOP_MULT, (void(*)(void)) Laplacian_2D_MF);CHKERRQ(ierr);
  ierr = PetscMalloc(sizeof(PetscQuadrature), &q);CHKERRQ(ierr);
  ierr = MatShellSetContext(A, (void *) q);CHKERRQ(ierr);
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  const Obj<ALE::Discretization>&          disc  = m->getDiscretization("u");
  const Obj<ALE::Mesh::real_section_type>& def   = m->getRealSection("default");
  const Obj<ALE::Mesh::real_section_type>& work1 = m->getRealSection("work1");
  const Obj<ALE::Mesh::real_section_type>& work2 = m->getRealSection("work2");
  q->numQuadPoints = disc->getQuadratureSize();
  q->quadPoints    = disc->getQuadraturePoints();
  q->quadWeights   = disc->getQuadratureWeights();
  q->numBasisFuncs = disc->getBasisSize();
  q->basis         = disc->getBasis();
  q->basisDer      = disc->getBasisDerivatives();
  work1->setAtlas(def->getAtlas());
  work1->allocateStorage();
  work2->setAtlas(def->getAtlas());
  work2->allocateStorage();
  PetscFunctionReturn(0);
}

EXTERN_C_BEGIN
#undef __FUNCT__
#define __FUNCT__ "Laplacian_2D_MF2"
PetscErrorCode Laplacian_2D_MF2(Mat A, Vec x, Vec y)
{
  Mesh           mesh;
  Obj<ALE::Mesh> m;
  Obj<ALE::Mesh::real_section_type> s;
  SectionReal    op, X, Y;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscObjectQuery((PetscObject) A, "mesh", (PetscObject *) &mesh);CHKERRQ(ierr);
  ierr = MatShellGetContext(A, (void **) &op);CHKERRQ(ierr);
  ierr = SectionRealGetSection(op, s);CHKERRQ(ierr);
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);

  ierr = MeshGetSectionReal(mesh, "work1", &X);CHKERRQ(ierr);
  ierr = MeshGetSectionReal(mesh, "work2", &Y);CHKERRQ(ierr);
  ierr = SectionRealToVec(X, mesh, SCATTER_REVERSE, x);CHKERRQ(ierr);

  const Obj<ALE::Mesh::label_sequence>& cells         = m->heightStratum(0);
  int                                   numBasisFuncs = m->getDiscretization("u")->getBasisSize();
  PetscScalar                          *elemVec;

  ierr = PetscMalloc(numBasisFuncs *sizeof(PetscScalar), &elemVec);CHKERRQ(ierr);
  // Loop over cells
  ierr = SectionRealZero(Y);CHKERRQ(ierr);
  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    const ALE::Mesh::real_section_type::value_type *elemMat = s->restrictPoint(*c_iter);
    PetscScalar *ev;

    ierr = SectionRealRestrict(X,  *c_iter, &ev);CHKERRQ(ierr);
    // Do local matvec
    for(int f = 0; f < numBasisFuncs; ++f) {
      elemVec[f] = 0.0;
      for(int g = 0; g < numBasisFuncs; ++g) {
        elemVec[f] += elemMat[f*numBasisFuncs+g]*ev[g];
      }
    }
    ierr = SectionRealUpdateAdd(Y, *c_iter, elemVec);CHKERRQ(ierr);
  }
  ierr = PetscFree(elemVec);CHKERRQ(ierr);
  ierr = SectionRealComplete(Y);CHKERRQ(ierr);

  ierr = SectionRealToVec(Y, mesh, SCATTER_FORWARD, y);CHKERRQ(ierr);
  ierr = SectionRealDestroy(X);CHKERRQ(ierr);
  ierr = SectionRealDestroy(Y);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}
EXTERN_C_END

#undef __FUNCT__
#define __FUNCT__ "Jac_Unstructured_Stored"
PetscErrorCode Jac_Unstructured_Stored(Mesh mesh, SectionReal section, Mat A, void *ctx)
{
  SectionReal    op;
  Obj<ALE::Mesh> m;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = MatShellSetOperation(A, MATOP_MULT, (void(*)(void)) Laplacian_2D_MF2);CHKERRQ(ierr);
  const Obj<ALE::Discretization>&          disc          = m->getDiscretization("u");
  const int                                numQuadPoints = disc->getQuadratureSize();
  const double                            *quadWeights   = disc->getQuadratureWeights();
  const int                                numBasisFuncs = disc->getBasisSize();
  const double                            *basisDer      = disc->getBasisDerivatives();
  const Obj<ALE::Mesh::real_section_type>& coordinates   = m->getRealSection("coordinates");
  const Obj<ALE::Mesh::label_sequence>&    cells         = m->heightStratum(0);
  const int dim = m->getDimension();
  double      *t_der, *b_der, *v0, *J, *invJ, detJ;
  PetscScalar *elemMat;

  ierr = MeshGetCellSectionReal(mesh, numBasisFuncs*numBasisFuncs, &op);CHKERRQ(ierr);
  ierr = MatShellSetContext(A, (void *) op);CHKERRQ(ierr);
  ierr = PetscMalloc(numBasisFuncs*numBasisFuncs * sizeof(PetscScalar), &elemMat);CHKERRQ(ierr);
  ierr = PetscMalloc5(dim,double,&t_der,dim,double,&b_der,dim,double,&v0,dim*dim,double,&J,dim*dim,double,&invJ);CHKERRQ(ierr);
  // Loop over cells
  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    ierr = PetscMemzero(elemMat, numBasisFuncs*numBasisFuncs * sizeof(PetscScalar));CHKERRQ(ierr);
    m->computeElementGeometry(coordinates, *c_iter, v0, J, invJ, detJ);
    // Loop over quadrature points
    for(int q = 0; q < numQuadPoints; ++q) {
      // Loop over trial functions
      for(int f = 0; f < numBasisFuncs; ++f) {
        for(int d = 0; d < dim; ++d) {
          t_der[d] = 0.0;
          for(int e = 0; e < dim; ++e) t_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+f)*dim+e];
        }
        // Loop over basis functions
        for(int g = 0; g < numBasisFuncs; ++g) {
          for(int d = 0; d < dim; ++d) {
            b_der[d] = 0.0;
            for(int e = 0; e < dim; ++e) b_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+g)*dim+e];
          }
          PetscScalar product = 0.0;
          for(int d = 0; d < dim; ++d) product += t_der[d]*b_der[d];
          elemMat[f*numBasisFuncs+g] += product*quadWeights[q]*detJ;
        }
      }
    }
    ierr = SectionRealUpdate(op, *c_iter, elemMat);CHKERRQ(ierr);
  }
  ierr = PetscFree(elemMat);CHKERRQ(ierr);
  ierr = PetscFree5(t_der,b_der,v0,J,invJ);CHKERRQ(ierr);

  const Obj<ALE::Mesh::real_section_type>& def   = m->getRealSection("default");
  const Obj<ALE::Mesh::real_section_type>& work1 = m->getRealSection("work1");
  const Obj<ALE::Mesh::real_section_type>& work2 = m->getRealSection("work2");
  work1->setAtlas(def->getAtlas());
  work1->allocateStorage();
  work2->setAtlas(def->getAtlas());
  work2->allocateStorage();
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "Jac_Unstructured"
PetscErrorCode Jac_Unstructured(Mesh mesh, SectionReal section, Mat A, void *ctx)
{
  Options       *options = (Options *) ctx;
  const double   lambda  = options->lambda;
  Obj<ALE::Mesh::real_section_type> s;
  Obj<ALE::Mesh> m;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MatZeroEntries(A);CHKERRQ(ierr);
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = SectionRealGetSection(section, s);CHKERRQ(ierr);
  const Obj<ALE::Discretization>&          disc          = m->getDiscretization("u");
  const int                                numQuadPoints = disc->getQuadratureSize();
  const double                            *quadWeights   = disc->getQuadratureWeights();
  const int                                numBasisFuncs = disc->getBasisSize();
  const double                            *basis         = disc->getBasis();
  const double                            *basisDer      = disc->getBasisDerivatives();
  const Obj<ALE::Mesh::real_section_type>& coordinates   = m->getRealSection("coordinates");
  const Obj<ALE::Mesh::label_sequence>&    cells         = m->heightStratum(0);
  const Obj<ALE::Mesh::order_type>&        order         = m->getFactory()->getGlobalOrder(m, "default", s);
  const int                                dim           = m->getDimension();
  double      *t_der, *b_der, *v0, *J, *invJ, detJ;
  PetscScalar *elemMat;

  ierr = PetscMalloc(numBasisFuncs*numBasisFuncs * sizeof(PetscScalar), &elemMat);CHKERRQ(ierr);
  ierr = PetscMalloc5(dim,double,&t_der,dim,double,&b_der,dim,double,&v0,dim*dim,double,&J,dim*dim,double,&invJ);CHKERRQ(ierr);
  // Loop over cells
  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    ierr = PetscMemzero(elemMat, numBasisFuncs*numBasisFuncs * sizeof(PetscScalar));CHKERRQ(ierr);
    m->computeElementGeometry(coordinates, *c_iter, v0, J, invJ, detJ);
    PetscScalar *u;

    ierr = SectionRealRestrict(section, *c_iter, &u);CHKERRQ(ierr);
    // Loop over quadrature points
    for(int q = 0; q < numQuadPoints; ++q) {
      PetscScalar fieldVal = 0.0;

      for(int f = 0; f < numBasisFuncs; ++f) {
        fieldVal += u[f]*basis[q*numBasisFuncs+f];
      }
      // Loop over trial functions
      for(int f = 0; f < numBasisFuncs; ++f) {
        for(int d = 0; d < dim; ++d) {
          t_der[d] = 0.0;
          for(int e = 0; e < dim; ++e) t_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+f)*dim+e];
        }
        // Loop over basis functions
        for(int g = 0; g < numBasisFuncs; ++g) {
          for(int d = 0; d < dim; ++d) {
            b_der[d] = 0.0;
            for(int e = 0; e < dim; ++e) b_der[d] += invJ[e*dim+d]*basisDer[(q*numBasisFuncs+g)*dim+e];
          }
          PetscScalar product = 0.0;
          for(int d = 0; d < dim; ++d) product += t_der[d]*b_der[d];
          elemMat[f*numBasisFuncs+g] += product*quadWeights[q]*detJ;
          // Nonlinear part
          if (lambda != 0.0) {
            elemMat[f*numBasisFuncs+g] -= basis[q*numBasisFuncs+f]*basis[q*numBasisFuncs+g]*lambda*PetscExpScalar(fieldVal)*quadWeights[q]*detJ;
          }
        }
      }
    }
    ierr = updateOperator(A, m, s, order, *c_iter, elemMat, ADD_VALUES);CHKERRQ(ierr);
  }
  ierr = PetscFree(elemMat);CHKERRQ(ierr);
  ierr = PetscFree5(t_der,b_der,v0,J,invJ);CHKERRQ(ierr);
  ierr = MatAssemblyBegin(A, MAT_FINAL_ASSEMBLY);CHKERRQ(ierr);
  ierr = MatAssemblyEnd(A, MAT_FINAL_ASSEMBLY);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#else

#undef __FUNCT__
#define __FUNCT__ "Jac_Unstructured"
PetscErrorCode Jac_Unstructured(Mesh mesh, SectionReal section, Mat A, void *ctx)
{
  Obj<ALE::Mesh> m;
  Obj<ALE::Mesh::real_section_type> s;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = SectionRealGetSection(section, s);CHKERRQ(ierr);
  FENICS_Jacobian(m, s, A, ctx);
  PetscFunctionReturn(0);
}
#endif

#undef __FUNCT__
#define __FUNCT__ "FormOperator"
PetscErrorCode FormOperator(DM dm, Options *options)
{
  Mesh           mesh = (Mesh) dm;
  SectionReal    X;
  Mat            J;
  PetscTruth     flag;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscOptionsHasName(PETSC_NULL, "-mat_view_draw", &flag);CHKERRQ(ierr);
  ierr = MeshGetSectionReal(mesh, "default", &X);CHKERRQ(ierr);
  ierr = SectionRealZero(X);CHKERRQ(ierr);
  ierr = MeshGetMatrix(mesh, MATAIJ, &J);CHKERRQ(ierr);
  ierr = Jac_Unstructured(mesh, X, J, options);CHKERRQ(ierr);
  if (flag) {ierr = MatView(J, PETSC_VIEWER_DRAW_WORLD);CHKERRQ(ierr);}
  ierr = MatDestroy(J);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "RunTests"
PetscErrorCode RunTests(DM dm, Options *options)
{
  PetscErrorCode ierr;

  PetscFunctionBegin;
  if (options->run == RUN_TEST) {
    ierr = FormFunctions(dm, options);CHKERRQ(ierr);
    ierr = FormWeakForms(dm, options);CHKERRQ(ierr);
    ierr = FormOperator(dm, options);CHKERRQ(ierr);
   }
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "CreateProblem"
PetscErrorCode CreateProblem(DM dm, Options *options)
{
  PetscFunctionBegin;
  if (options->dim == 2) {
    if (options->bcType == DIRICHLET) {
      if (options->lambda > 0.0) {
        options->func    = nonlinear_2d;
        options->exactFunc = quadratic_2d;
      } else if (options->reentrantMesh) { 
        options->func = singularity_2d;
        options->exactFunc = singularity_exact_2d;
      } else {
        options->func    = constant;
        options->exactFunc = quadratic_2d;
      }
    } else {
      options->func      = linear_2d;
      options->exactFunc = cubic_2d;
    }
  } else if (options->dim == 3) {
    if (options->bcType == DIRICHLET) {
      if (options->reentrantMesh) {
        options->func = singularity_3d;
        options->exactFunc = singularity_exact_3d;
      } else {
        if (options->lambda > 0.0) {
          options->func    = nonlinear_3d;
        } else {
          options->func    = constant;
        }
        options->exactFunc = quadratic_3d;
      }
    } else {
      options->func      = linear_3d;
      options->exactFunc = cubic_3d;
    }
  } else {
    SETERRQ1(PETSC_ERR_SUP, "Dimension not supported: %d", options->dim);
  }
  Mesh           mesh = (Mesh) dm;
  Obj<ALE::Mesh> m;
  int            numBC = (options->bcType == DIRICHLET) ? 1 : 0;
  int            markers[1]  = {1};
  double       (*funcs[1])(const double *coords) = {options->exactFunc};
  PetscErrorCode ierr;

  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  if (options->dim == 1) {
    ierr = CreateProblem_gen_0(dm, "u", numBC, markers, funcs, options->exactFunc);CHKERRQ(ierr);
    options->integrate = IntegrateDualBasis_gen_0;
  } else if (options->dim == 2) {
    ierr = CreateProblem_gen_1(dm, "u", numBC, markers, funcs, options->exactFunc);CHKERRQ(ierr);
    options->integrate = IntegrateDualBasis_gen_1;
  } else if (options->dim == 3) {
    ierr = CreateProblem_gen_2(dm, "u", numBC, markers, funcs, options->exactFunc);CHKERRQ(ierr);
    options->integrate = IntegrateDualBasis_gen_2;
  } else {
    SETERRQ1(PETSC_ERR_SUP, "Dimension not supported: %d", options->dim);
  }
  const ALE::Obj<ALE::Mesh::real_section_type> s = m->getRealSection("default");
  s->setDebug(options->debug);
  m->setupField(s);
  if (options->debug) {s->view("Default field");}
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "CreateExactSolution"
PetscErrorCode CreateExactSolution(DM dm, Options *options)
{
  Mesh           mesh = (Mesh) dm;
  Obj<ALE::Mesh> m;
  Obj<ALE::Mesh::real_section_type> s;
  const int      dim = options->dim;
  PetscTruth     flag;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = MeshGetMesh(mesh, m);CHKERRQ(ierr);
  ierr = MeshGetSectionReal(mesh, "exactSolution", &options->exactSol.section);CHKERRQ(ierr);
  ierr = SectionRealGetSection(options->exactSol.section, s);CHKERRQ(ierr);
  m->setupField(s);
  const Obj<ALE::Mesh::label_sequence>&     cells       = m->heightStratum(0);
  const Obj<ALE::Mesh::real_section_type>&  coordinates = m->getRealSection("coordinates");
  const int                                 localDof    = m->sizeWithBC(s, *cells->begin());
  ALE::Mesh::real_section_type::value_type *values      = new ALE::Mesh::real_section_type::value_type[localDof];
  double                                   *v0          = new double[dim];
  double                                   *J           = new double[dim*dim];
  double                                    detJ;

  for(ALE::Mesh::label_sequence::iterator c_iter = cells->begin(); c_iter != cells->end(); ++c_iter) {
    const Obj<ALE::Mesh::coneArray>      closure = ALE::SieveAlg<ALE::Mesh>::closure(m, *c_iter);
    const ALE::Mesh::coneArray::iterator end     = closure->end();
    int                                  v       = 0;

    m->computeElementGeometry(coordinates, *c_iter, v0, J, PETSC_NULL, detJ);
    for(ALE::Mesh::coneArray::iterator cl_iter = closure->begin(); cl_iter != end; ++cl_iter) {
      const int pointDim = s->getFiberDimension(*cl_iter);

      if (pointDim) {
        for(int d = 0; d < pointDim; ++d, ++v) {
          values[v] = (*options->integrate)(v0, J, v, options->exactFunc);
        }
      }
    }
    m->updateAll(s, *c_iter, values);
  }
  delete [] values;
  delete [] v0;
  delete [] J;
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view", &flag);CHKERRQ(ierr);
  if (flag) {s->view("Exact Solution");}
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view_vtk", &flag);CHKERRQ(ierr);
  if (flag) {ierr = ViewSection(mesh, options->exactSol.section, "exact_sol.vtk");CHKERRQ(ierr);}
  ierr = MeshGetSectionReal(mesh, "error", &options->error.section);CHKERRQ(ierr);
  ierr = SectionRealGetSection(options->error.section, s);CHKERRQ(ierr);
  s->setFiberDimension(m->heightStratum(0), 1);
  m->allocate(s);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "CheckError"
PetscErrorCode CheckError(DM dm, ExactSolType sol, Options *options)
{
  Mesh           mesh = (Mesh) dm;
  MPI_Comm       comm;
  const char    *name;
  PetscScalar    norm;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscObjectGetComm((PetscObject) dm, &comm);CHKERRQ(ierr);
  ierr = CalculateError(mesh, sol.section, &norm, options);CHKERRQ(ierr);
  ierr = PetscObjectGetName((PetscObject) sol.section, &name);CHKERRQ(ierr);
  PetscPrintf(comm, "Error for trial solution %s: %g\n", name, norm);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "CheckResidual"
PetscErrorCode CheckResidual(DM dm, ExactSolType sol, Options *options)
{
  Mesh           mesh = (Mesh) dm;
  SectionReal    residual;
  MPI_Comm       comm;
  const char    *name;
  PetscScalar    norm;
  PetscTruth     flag;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscObjectGetComm((PetscObject) dm, &comm);CHKERRQ(ierr);
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view", &flag);CHKERRQ(ierr);
  ierr = SectionRealDuplicate(sol.section, &residual);CHKERRQ(ierr);
  ierr = PetscObjectSetName((PetscObject) residual, "residual");CHKERRQ(ierr);
  ierr = Rhs_Unstructured(mesh, sol.section, residual, options);CHKERRQ(ierr);
  if (flag) {ierr = SectionRealView(residual, PETSC_VIEWER_STDOUT_WORLD);CHKERRQ(ierr);}
  ierr = SectionRealNorm(residual, mesh, NORM_2, &norm);CHKERRQ(ierr);
  ierr = SectionRealDestroy(residual);CHKERRQ(ierr);
  ierr = PetscObjectGetName((PetscObject) sol.section, &name);CHKERRQ(ierr);
  PetscPrintf(comm, "Residual for trial solution %s: %g\n", name, norm);
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "CreateSolver"
PetscErrorCode CreateSolver(DM dm, DMMG **dmmg, Options *options)
{
  MPI_Comm       comm;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscObjectGetComm((PetscObject) dm, &comm);CHKERRQ(ierr);
  ierr = DMMGCreate(comm, 1, options, dmmg);CHKERRQ(ierr);
  ierr = DMMGSetDM(*dmmg, dm);CHKERRQ(ierr);
  if (options->operatorAssembly == ASSEMBLY_FULL) {
    ierr = DMMGSetSNESLocal(*dmmg, Rhs_Unstructured, Jac_Unstructured, 0, 0);CHKERRQ(ierr);
#if 0
  } else if (options->operatorAssembly == ASSEMBLY_CALCULATED) {
    ierr = DMMGSetMatType(*dmmg, MATSHELL);CHKERRQ(ierr);
    ierr = DMMGSetSNESLocal(*dmmg, Rhs_Unstructured, FENICS_Jacobian_Calculated, 0, 0);CHKERRQ(ierr);
  } else if (options->operatorAssembly == ASSEMBLY_STORED) {
    ierr = DMMGSetMatType(*dmmg, MATSHELL);CHKERRQ(ierr);
    ierr = DMMGSetSNESLocal(*dmmg, Rhs_Unstructured, FENICS_Jacobian_Stored, 0, 0);CHKERRQ(ierr);
#endif
  } else {
    SETERRQ1(PETSC_ERR_ARG_WRONG, "Assembly type not supported: %d", options->operatorAssembly);
  }
  if (options->bcType == NEUMANN) {
    // With Neumann conditions, we tell DMMG that constants are in the null space of the operator
    ierr = DMMGSetNullSpace(*dmmg, PETSC_TRUE, 0, PETSC_NULL);CHKERRQ(ierr);
  }
  PetscFunctionReturn(0);
}

#undef __FUNCT__
#define __FUNCT__ "Solve"
PetscErrorCode Solve(DMMG *dmmg, Options *options)
{
  Mesh                mesh = (Mesh) DMMGGetDM(dmmg);
  SectionReal         solution;
  Obj<ALE::Mesh::real_section_type> sol;
  double              error;
  SNES                snes;
  MPI_Comm            comm;
  PetscInt            its;
  PetscTruth          flag;
  SNESConvergedReason reason;
  PetscErrorCode      ierr;

  PetscFunctionBegin;
  ierr = DMMGSolve(dmmg);CHKERRQ(ierr);
  snes = DMMGGetSNES(dmmg);
  ierr = SNESGetIterationNumber(snes, &its);CHKERRQ(ierr);
  ierr = SNESGetConvergedReason(snes, &reason);CHKERRQ(ierr);
  ierr = PetscObjectGetComm((PetscObject) snes, &comm);CHKERRQ(ierr);
  ierr = PetscPrintf(comm, "Number of nonlinear iterations = %D\n", its);CHKERRQ(ierr);
  ierr = PetscPrintf(comm, "Reason for solver termination: %s\n", SNESConvergedReasons[reason]);CHKERRQ(ierr);
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view", &flag);CHKERRQ(ierr);
  if (flag) {ierr = VecView(DMMGGetx(dmmg), PETSC_VIEWER_STDOUT_WORLD);CHKERRQ(ierr);}
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view_draw", &flag);CHKERRQ(ierr);
  if (flag && options->dim == 2) {ierr = VecView(DMMGGetx(dmmg), PETSC_VIEWER_DRAW_WORLD);CHKERRQ(ierr);}
  ierr = MeshGetSectionReal(mesh, "default", &solution);CHKERRQ(ierr);
  ierr = SectionRealGetSection(solution, sol);CHKERRQ(ierr);
  ierr = SectionRealToVec(solution, mesh, SCATTER_REVERSE, DMMGGetx(dmmg));CHKERRQ(ierr);
  ierr = CalculateError(mesh, solution, &error, options);CHKERRQ(ierr);
  ierr = PetscPrintf(sol->comm(), "Total error: %g\n", error);CHKERRQ(ierr);
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view_vtk", &flag);CHKERRQ(ierr);
  if (flag) {
    ierr = ViewSection(mesh, solution, "sol.vtk");CHKERRQ(ierr);
    ierr = ViewSection(mesh, options->error.section, "error.vtk", false);CHKERRQ(ierr);
  }
  ierr = PetscOptionsHasName(PETSC_NULL, "-vec_view", &flag);CHKERRQ(ierr);
  if (flag) {sol->view("Solution");}
  ierr = PetscOptionsHasName(PETSC_NULL, "-hierarchy_vtk", &flag);CHKERRQ(ierr);
  if (flag) {
    PetscViewer    viewer;
    ierr = PetscViewerCreate(sol->comm(), &viewer);CHKERRQ(ierr);
    ierr = PetscViewerSetType(viewer, PETSC_VIEWER_ASCII);CHKERRQ(ierr);
    ierr = PetscViewerSetFormat(viewer, PETSC_VIEWER_ASCII_VTK);CHKERRQ(ierr);
    ierr = PetscViewerFileSetName(viewer, "mesh_hierarchy.vtk");CHKERRQ(ierr);
    double offset[3] = {2.0, 0.0, 0.25};
    ierr = PetscOptionsReal("-hierarchy_vtk", PETSC_NULL, "bratu.cxx", *offset, offset, PETSC_NULL);CHKERRQ(ierr);
    ierr = VTKViewer::writeHeader(viewer);CHKERRQ(ierr);
    ierr = VTKViewer::writeHierarchyVertices(dmmg, viewer, offset);CHKERRQ(ierr);
    ierr = VTKViewer::writeHierarchyElements(dmmg, viewer);CHKERRQ(ierr);
    ierr = PetscViewerDestroy(viewer);CHKERRQ(ierr);
  }
  ierr = SectionRealDestroy(solution);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}


#undef __FUNCT__
#define __FUNCT__ "main"
int main(int argc, char *argv[])
{
  MPI_Comm       comm;
  Options        options;
  DM             dm;
  PetscErrorCode ierr;

  PetscFunctionBegin;
  ierr = PetscInitialize(&argc, &argv, (char *) 0, help);CHKERRQ(ierr);
  comm = PETSC_COMM_WORLD;
  ierr = ProcessOptions(comm, &options);CHKERRQ(ierr);
  try {
    ierr = CreateMesh(comm, &dm, &options);CHKERRQ(ierr);
    ierr = CreateProblem(dm, &options);CHKERRQ(ierr);
    ierr = RunTests(dm, &options);CHKERRQ(ierr);
    if (options.run == RUN_FULL) {
      DMMG *dmmg;

      ierr = CreateExactSolution(dm, &options);CHKERRQ(ierr);
      ierr = CheckError(dm, options.exactSol, &options);CHKERRQ(ierr);
      ierr = CheckResidual(dm, options.exactSol, &options);CHKERRQ(ierr);
      ierr = CreateSolver(dm, &dmmg, &options);CHKERRQ(ierr);
      ierr = Solve(dmmg, &options);CHKERRQ(ierr);
      ierr = DMMGDestroy(dmmg);CHKERRQ(ierr);
      ierr = DestroyExactSolution(options.exactSol, &options);CHKERRQ(ierr);
      ierr = DestroyExactSolution(options.error,    &options);CHKERRQ(ierr);
    }
    ierr = DestroyMesh(dm, &options);CHKERRQ(ierr);
  } catch(ALE::Exception e) {
    std::cerr << e << std::endl;
  }
  ierr = PetscFinalize();CHKERRQ(ierr);
  PetscFunctionReturn(0);
}
