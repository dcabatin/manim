from functools import reduce
import itertools as it
import operator as op
import copy
import numpy as np
import random

from manimlib.imports import *
from kuratowski.our_discrete_graph_scene import *



class TwoConnectedLemmaBase(Graph):
    def construct(self):

        u = (-2, 0, 0)
        v = (2, 0, 0)

        self.vertices = [u,v]
        
        upper_arc = [u]
        for i in range(4):
            angle = (PI/5)*(4-i)
            upper_arc.append((2*np.cos(angle), 2*np.sin(angle), 0))
        upper_arc.append(v)

        self.vertices = upper_arc 

        self.edges = [(0,5)] + [(i,i+1) for i in range(5)]

        self.dashed = [(2,3)]


class TwoConnectedInductive(Graph):
    def construct(self):

        u = (-2.5, 0, 0)
        v = (2.5, 0, 0)
        w = (1.5, 0, 0)
        

        self.vertices = [
            u, (-1.5, 0, 0), (-0.5, 0, 0), (0.5, 0, 0), w, v
        ]

        uw_arc = [
            (2*np.cos(angle)-0.5, 2*np.sin(angle), 0)
            for angle in [4*PI/5, 3*PI/5, 2*PI/5, PI/5]
        ]

        self.vertices.extend(uw_arc)

        vu_arc = [
            (1.25*np.cos(angle)+1.25, 1.25*np.sin(angle), 0)
            for angle in [5*PI/3, 4*PI/3]
        ]

        self.vertices.extend(vu_arc)
        self.vertices.append((0,0,0))

        self.edges = [
            (0,1), (1,2), (2,3), (3,4), (4,5), #straight line
            (0,6), (6,7), (7,8), (8,9), (9,4), #uw arc
            (5,10), (10,11), (11,12)
        ]

        self.dashed = [(2,3), (7,8), (10,11)]


class TwoConnectedLemma(OurGraphTheory):

    def construct(self):
        self.graph = TwoConnectedLemmaBase()
        super().construct()
        self.shift_graph(DOWN + LEFT*2.5)


        thm = TextMobject("Theorem: in a $2$-connected graph, any pair of vertices is contained in a cycle.", alignment="\\centering")
        thm.scale(0.75)
        thm.shift(UP*3)
        self.play(Write(thm, run_time=1))

        #--------- Base Case ----------------------

        #Draw u and v on screen
        u, v = self.vertices[0], self.vertices[5]
        u_label, v_label = (TextMobject("$u$").next_to(u, DL),
                            TextMobject("$v$").next_to(v, DR))
        self.play(Write(u_label), Write(v_label), *self.draw([u,v], play=False))

        self.wait(6)

        base_case = TextMobject("Base Case:\\\\ $u,v$ are adjacent", alignment="\\justify")
        base_case.shift(RIGHT*4)
        base_case.scale(0.8)
        self.play(Write(base_case))

        #Draw then erase edge from u to v
        self.draw([self.edges[0]])
        self.wait(4)

        #Draw alternate path from u to v
        self.erase_copy([self.edges[0]], run_time=0.4)
        self.play(
            AnimationGroup(
                *self.draw(self.vertices[1:-1], play=False, run_time=0.5),
                *self.draw(self.edges[1:], play=False, run_time=0.5),
                lag_ratio=0.4)
        )
        self.wait(4)

        #Complete path with edge uv
        self.draw(self.edges[0], reverse=True)

        #Trace the cycle
        cycle = self.trace_cycle([0,1,2,3,4,5,0], run_time=1)
        self.play(*[FadeOut(c, run_time=0.5) for c in cycle])
        self.wait(7)

        self.erase_copy(self.vertices[1:-1] + self.edges)
        
        #------------------ Inductive Step --------------------
        self.graph =TwoConnectedInductive()
        super().construct()
        self.shift_graph(DOWN + LEFT*2.5)

        inductive_case = TextMobject("Inductive Step:\\\\ $u,v$ have distance $d+1$", alignment="\\justify")
        inductive_case.shift(RIGHT*4)
        inductive_case.scale(0.8)

        # Transition to new graph
        new_u, new_v = self.vertices[0], self.vertices[5]
        new_u_lab, new_v_lab = (TextMobject("$u$").next_to(new_u, DL),
                                TextMobject("$v$").next_to(new_v, DR))
        inductive_trans = [
            ReplacementTransform(u, new_u),
            ReplacementTransform(v, new_v),
            ReplacementTransform(u_label, new_u_lab),
            ReplacementTransform(v_label, new_v_lab),
            Transform(base_case, inductive_case)
        ]
        self.play(*inductive_trans)

        # Draw initial path from u to v
        self.play(
            AnimationGroup(
                *self.draw(self.vertices[1:5], play=False, run_time=0.5),
                *self.draw(self.edges[:5], play=False, run_time=0.5),
                lag_ratio=0.4
            )
        )
        
        
        # Draw brace to label distance
        brace = BraceLabel(VGroup(*self.vertices), "d+1")
        self.draw(brace)
        self.wait(5)
        
        # Label w
        w = self.vertices[4]
        w_label = TextMobject("$w$").next_to(w, DOWN)
        self.play(Write(w_label))

        # Make brace smaller
        self.play(Transform(brace, BraceLabel(VGroup(new_u, w, self.vertices[11]), "d")))
        self.wait(4)

        # Draw uw arc
        self.play(
            AnimationGroup(
                *self.draw(self.vertices[6:10], play=False, run_time=0.5),
                *self.draw(self.edges[5:10], play=False, run_time=0.5),
                lag_ratio=0.4
            )
        )

        # Trace uw cycle
        cycle = self.trace_cycle([0, 6, 7, 8, 9, 4, 3, 2, 1, 0])
        self.play(*[FadeOut(c, run_time=0.5) for c in cycle])
        self.wait(5)

        # Cut w
        self.erase_copy([w, self.edges[9], w_label, brace] + self.edges[3:5])
        self.wait(4)

        # Draw path from v to u 
        self.play(
            AnimationGroup(
                *self.draw(self.vertices[10:12], play=False, run_time=0.5),
                *self.draw(self.edges[10:13], play=False, run_time=0.5),
                lag_ratio=0.4
            )
        )
        w_label = TextMobject("$w$").next_to(w, DOWN)
        self.draw([self.vertices[4], self.edges[9], w_label] + self.edges[3:5])
        self.wait(5)

        #Trace final cycle
        cycle = self.trace_cycle([0, 6, 7, 8, 9, 4, 5, 10, 11, 12, 2, 1, 0])
        self.play(*[FadeOut(c, run_time=0.5) for c in cycle])
        self.wait()

        self.erase_copy(self.vertices[:-1]+self.edges+[u_label, v_label, w_label])
        self.wait()
    


