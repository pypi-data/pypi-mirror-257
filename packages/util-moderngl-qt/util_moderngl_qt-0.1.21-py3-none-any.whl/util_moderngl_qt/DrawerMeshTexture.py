"""
OpenGL drawer of uniform simplex mesh (triangles and line segments) with texture
"""

import typing
from pyrr import Matrix44
import numpy
import moderngl


class ElementInfo:

    def __init__(self, index: numpy.ndarray, mode, color):
        self.vao = None
        # index should be numpy.uint32
        if index.dtype == numpy.uint32:
            self.index = index
        else:
            self.index = index.astype(numpy.uint32)
        self.mode = mode
        self.color = color


class Drawer:

    def __init__(self,
                 list_elem2vtx: typing.List[ElementInfo],
                 vtx2xyz: numpy.ndarray,
                 vtx2uv: numpy.ndarray):
        # coordinate
        assert len(vtx2xyz.shape) == 2
        if vtx2xyz.dtype == numpy.float32:
            self.vtx2xyz = vtx2xyz
        else:
            self.vtx2xyz = vtx2xyz.astype(numpy.float32)
        # uv coordinate
        assert len(vtx2uv.shape) == 2
        assert vtx2uv.shape[0] == vtx2xyz.shape[0]
        assert vtx2uv.shape[1] == 2
        if vtx2uv.dtype == numpy.float32:
            self.vtx2uv = vtx2uv
        else:
            self.vtx2uv = vtx2uv.astype(numpy.float32)
        self.list_elem2vtx = list_elem2vtx
        self.vao_content = None

    def init_gl(self, ctx: moderngl.Context):
        self.prog = ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 Mvp;
                in vec2 in_uv;
                in vec3 in_xyz;
                out vec2 texPrj;
                void main() {
                    gl_Position = Mvp * vec4(in_xyz, 1.0);
                    texPrj = in_uv;
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D myTextureSampler;
                uniform vec3 color;
                uniform bool is_texture;
                out vec4 f_color;
                in vec2 texPrj;
                void main() {
                    if( is_texture ) {                 
                        f_color = texture(myTextureSampler,texPrj);
                    }
                    else { 
                        f_color = vec4(color, 1.0);
                    }
                }
            '''
        )

        self.vao_content = [
            (ctx.buffer(self.vtx2xyz.tobytes()), f'{self.vtx2xyz.shape[1]}f', 'in_xyz'),
            (ctx.buffer(self.vtx2uv.tobytes()), '2f', 'in_uv')
        ]
        #del self.vtx2xyz
        #del self.vtx2uv
        for el in self.list_elem2vtx:
            index_buffer = ctx.buffer(el.index.tobytes())
            el.vao = ctx.vertex_array(
                self.prog, self.vao_content, index_buffer, 4
            )
            #del el.index

    def update_position(self, vtx2xyz: numpy.ndarray):
        if vtx2xyz.dtype != numpy.float32:
            vtx2xyz = vtx2xyz.astype(numpy.float32)
        if self.vao_content != None:
            vbo = self.vao_content[0][0]
            vbo.write(vtx2xyz.tobytes())

    def paint_gl_texture(self, mvp: Matrix44, texture_location: int):
        self.prog['Mvp'].value = tuple(mvp.flatten())
        self.prog['myTextureSampler'].value = texture_location
        for el in self.list_elem2vtx:
            if el.color is None:
                self.prog['is_texture'].value = True
            else:
                self.prog['is_texture'].value = False
                self.prog['color'] = el.color
            el.vao.render(mode=el.mode)
