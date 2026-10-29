import ast
import textwrap
from pathlib import Path
p=Path('src/robot4_task_yamada/src/auto_move.py')
s=p.read_text()
tree=ast.parse(s)
cls=next(n for n in tree.body if isinstance(n,ast.ClassDef))
methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
lines=s.splitlines()
def method(name):
    n=methods[name]
    out=textwrap.dedent('\n'.join(lines[n.lineno-1:n.end_lineno]))
    out=out.replace('(self, message)', '(message)').replace('(self)', '()')
    for attr in ('observation','camera','pose'):
        out=out.replace('self.'+attr,'latest_'+attr)
    return out.replace('self.','')
prefix='\n'.join(lines[:cls.lineno-1]).replace('import numpy as np\n','')
globals_code='''# コールバックとメインループで共有するセンサ情報
bridge = CvBridge()
lock = threading.Lock()
latest_observation = None
latest_camera = None
latest_pose = None
min_area = 8.0
pub = None
debug_pub = None
'''
callbacks=[]
for name, var in [('camera_callback','latest_camera'),('odom_callback','latest_pose'),('image_callback','latest_observation')]:
    out=method(name)
    a,b=out.split('\n',1)
    callbacks.append(a+'\n    global '+var+'\n'+b)
callbacks.append(method('stop'))
init=method('__init__').split('\n',1)[1]
init_lines=init.splitlines()
init_lines=[l for l in init_lines if not any(l.strip().startswith(x+' =') for x in ('bridge','lock','latest_observation','latest_camera','latest_pose'))]
run=method('run').split('\n',1)[1]
main='''def main():
    global min_area, pub, debug_pub
    rospy.init_node('ball_collector')
'''+ '\n'.join(init_lines)+'\n\n'+run
p.write_text(prefix+'\n'+globals_code+'\n\n'+'\n\n\n'.join(callbacks)+'\n\n\n'+main+'''


if __name__ == '__main__':
    try:
        main()
    except (rospy.ROSInterruptException, rospy.ROSException, rospy.ServiceException) as error:
        if not rospy.is_shutdown():
            rospy.logerr('Ball collector stopped: %s', error)
            raise
''')
ast.parse(p.read_text())
