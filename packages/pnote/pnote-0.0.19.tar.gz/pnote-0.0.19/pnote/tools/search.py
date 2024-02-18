from pnote.tools.tool import Tool
import argparse

class ToolSearch(Tool):

    def add_parser(self,subparsers):
        p = subparsers.add_parser("search", description="Perform search operation on your notes")
        p.add_argument("-g", "--grep", help="Grep an expression")
        p.add_argument("-n", "--name", help="Search for a note path")
        p.add_argument("-t", "--tag", help="Search for a note with a tag")
        p.add_argument("-c", "--content", help="Show content only", action='store_true')
        p.add_argument("--last", help="Get last n note files")
        p.add_argument("--first", help="Get first n note files")

    def run(self, project, args):
        if args.grep:
            first=True
            for entry in project.grep(args.grep):
                subpath=entry[0]
                if not args.content:
                    if not first:
                        print()
                    print("=> "+subpath)
                for line in entry[1]:
                    ln=line[0]
                    content=line[1]
                    if args.content:
                        print(content)
                    else:
                        print("L{}: {}".format(ln,content))
                first=False
        elif args.tag:
            first=True
            for subpath in project.searchtag(args.tag):
                if not args.content:
                    if not first:
                        print()
                    print("=> "+subpath)
                with open(project.getpath(subpath),"r") as fp:
                    for line in fp:
                        print(line,end="")
                first=False
        elif args.last:
            subpaths=project.find(None)
            for subpath in subpaths[-abs(int(args.last)):]:
                print(subpath)
        elif args.first:
            subpaths=project.find(None)
            for subpath in subpaths[:abs(int(args.first))]:
                print(subpath)
        else:
            if args.name:
                [ print(subpath) for subpath in project.find(args.name) ]
            else:
                [ print(subpath) for subpath in project.find(None) ]


