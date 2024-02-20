import json
import time
import traceback
from mupy.test_runners import my_oracle_runner, unittest_runner
from mupy.utils import ast
from flask import Flask, Response, request
from flask_cors import CORS
from mupy.mutation.finders import arith_op_finders, const_finders, comp_op_finders, bool_op_finders
from mupy.mutation.mutators import arith_op_mutator, bool_op_mutator, comp_op_mutator, const_mutator


app = Flask(__name__, static_folder='static', static_url_path="/")
CORS(app)  # Enable CORS for all routes

# Your existing code...


def emit(mutant, check=True):
    if(check and mutant['mutant'] == mutant['original']):
        return ''
    return f'{json.dumps(mutant)}\n\n'



@app.route('/')
def hello():
  return app.send_static_file("index.html")

@app.route('/mutate',methods=['POST'])
def mutate():
   
    data = request.get_json()
    print(data)
    program = data.get('program')

    def get_mutants():

       
        try:
            main_node = ast.get_ast(program)
            program_parsed = ast.get_program_string(main_node)
        except Exception as e:
            yield emit({'id': 'src', 'error': [str(e), traceback.format_exc()]}, False)
            return
          

        
        # Generate the mutants
        arith_nodes = arith_op_finders.find_arithmetic_operators(main_node)
        bool_nodes = bool_op_finders.find_bool_operators(main_node)
        comp_nodes = comp_op_finders.find_comparison_operators(main_node)
        const_nodes = const_finders.find_constants(main_node)


        # Mutate the nodes
        mutations = []
        
        nodecount=0
        for node in arith_nodes:
            nodecount += 1
            mutants = arith_op_mutator.mutate_arithmetic_operators(node, main_node)
            # Prepare a json data {original: program, mutant: mutant, id: "arithmetique/mutant1.py"}
            count = 0
            for mutant in mutants:
                count += 1
                yield emit({'original': program_parsed, 'mutant': ast.get_program_string(mutant), 'id': f'arithmetique/node{nodecount}/mutant_{count}.py'})
                #wait for 2ms
                time.sleep(0.002)
    
        for node in bool_nodes:
            nodecount += 1
            mutants = bool_op_mutator.replace_bool_op(node, main_node)
            # Prepare a json data {original: program, mutant: mutant, id: "bool/mutant1.py"}
            count = 0
            for mutant in mutants:
                count += 1
                yield emit({'original': program_parsed, 'mutant': ast.get_program_string(mutant), 'id': f'bool/node{nodecount}/mutant_{count}.py'})
                #wait for 2ms
                time.sleep(0.002)
        
        for node in comp_nodes:
            nodecount += 1
            mutants = comp_op_mutator.replace_comp_op(node, main_node)
            # Prepare a json data {original: program, mutant: mutant, id: "comp/mutant1.py"}
            count = 0
            for mutant in mutants:
                count += 1
                yield emit({'original': program_parsed, 'mutant': ast.get_program_string(mutant), 'id': f'comp/node{nodecount}/mutant_{count}.py'})
                #wait for 2ms
                time.sleep(0.002)
        
        for node in const_nodes:
            nodecount += 1
            mutants = const_mutator.mutate_constants(node, main_node)
            # Prepare a json data {original: program, mutant: mutant, id: "const/mutant1.py"}
            count = 0
            for mutant in mutants:
                count += 1
                yield emit({'original': program_parsed, 'mutant': ast.get_program_string(mutant), 'id': f'const/node{nodecount}/mutant_{count}.py'})
                #wait for 2ms
                time.sleep(0.002)
        
    return Response(get_mutants(), mimetype="text/event-stream")






@app.route('/parse', methods=['POST'])
def parse():
    data = request.get_json()
    print(data)
    program = data.get('program')
    node = ast.get_ast(program)
    program_parsed = ast.get_program_string(node)
    return json.dumps({'original': program, 'parsed': program_parsed})



@app.route('/test', methods=['POST'])
def test_runner():
    print('Testing the mutants')
    try :
        request.get_json()
    except Exception as e:
        print('Error in the request')
        print(e)
        return json.dumps({'error': 'Error in the request'})
    
    data = request.get_json()
    print('Testing the mutants')
    print(data)
    programs = data.get('programs')
    test = data.get('test')
   
    def runtest():
        # the programs is a json string like this: [{id: "arithmetique/mutant1.py", program: "def add(a, b):\n    return a + b\n"}]
        # the test is a string like this: "def test_add():\n    assert add(1, 2) == 3\n"

        for program in programs:
            mutation = program['program']
            id = program['id']
            try:
                output = unittest_runner.run_tests(test, mutation)

                if len(output) > 0:
                    print(f'Mutant Killed by the test suite')
                    yield emit({'id': id, 'success': False, 'output': output}, False)
                else:
                    print(f'Mutant survived')
                    yield emit({'id': id, 'success': True, 'output': output}, False)
            except Exception as e:
                stack = traceback.format_exc()
                yield emit({'id': id, 'success': False, 'output': [],  'error': [str(e), str(stack)]}, False)

    return Response(runtest(), mimetype="text/event-stream")

        

    


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)