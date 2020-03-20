import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from std_mgmt.student.models import University, Student

# Create a GraphQL type for the actor model
class UniversityType(DjangoObjectType):
    class Meta:
        model = University

# Create a GraphQL type for the movie model
class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        
        
        
        
class Query(ObjectType):
    university = graphene.Field(UniversityType, id=graphene.Int())
    student = graphene.Field(StudentType, id=graphene.Int())
    universities = graphene.List(UniversityType)
    students= graphene.List(StudentType)

    def resolve_university(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return University.objects.get(pk=id)

        return None

    def resolve_student(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Student.objects.get(pk=id)

        return None

    def resolve_universities(self, info, **kwargs):
        return University.objects.all()

    def resolve_students(self, info, **kwargs):
        return Student.objects.all()
        
        
        



class UniversityInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()

class StudentInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    universities = graphene.List(UniversityInput)




class CreateUniversity(graphene.Mutation):
    class Arguments:
        input = UniversityInput(required=True)

    ok = graphene.Boolean()
    universities = graphene.Field(UniversityType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        university_instance = University(name=input.name)
        university_instance.save()
        return CreateUniversity(ok=ok, universities=university_instance)

class UpdateUniversity(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UniversityInput(required=True)

    ok = graphene.Boolean()
    university = graphene.Field(UniversityType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        university_instance = University.objects.get(pk=id)
        if university_instance:
            ok = True
            university_instance.name = input.name
            university_instance.save()
            return UpdateUniversity(ok=ok, universities=university_instance)
        return UpdateUniversity(ok=ok, universities=None)
        
        
        
        
        
class CreateStudent(graphene.Mutation):
    class Arguments:
        input = StudentInput(required=True)

    ok = graphene.Boolean()
    student = graphene.Field(StudentType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        universities = []
        for university_input in input.universities:
          university = University.objects.get(pk=university_input.id)
          if university is None:
            return CreateStudent(ok=False, student=None)
          universities.append(university)
        student_instance = Student(
          name=input.name
          )
        student_instance.save()
        student_instance.universities.set(universities)
        return CreateStudent(ok=ok, student=student_instance)


class UpdateStudent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = StudentInput(required=True)

    ok = graphene.Boolean()
    student = graphene.Field(StudentType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        student_instance = Student.objects.get(pk=id)
        if student_instance:
            ok = True
            universities = []
            for university_input in input.universities:
              university = University.objects.get(pk=university_input.id)
              if university is None:
                return UpdateStudent(ok=False, student=None)
              universities.append(university)
            student_instance.name=input.name
            student_instance.universities.set(universities)
            return UpdateStudent(ok=ok, student=student_instance)
        return UpdateStudent(ok=ok, student=None)
        




class Mutation(graphene.ObjectType):
    create_university = CreateUniversity.Field()
    update_university = UpdateUniversity.Field()
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    
    
    
schema = graphene.Schema(query=Query, mutation=Mutation)